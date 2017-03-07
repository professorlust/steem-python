# coding=utf-8
import concurrent.futures
import json
import logging
import socket
from functools import partial
from itertools import cycle
from urllib.parse import urlparse
import time

import certifi
import urllib3
from steembase.exceptions import RPCError
from urllib3.connection import HTTPConnection
from urllib3.exceptions import MaxRetryError

logger = logging.getLogger(__name__)


class HttpClient(object):
    """Simple Steem JSON-HTTP-RPC API

        This class serves as an abstraction layer for easy use of the
        Steem API.

    Args:
      nodes (list): A list of Steem HTTP RPC nodes to connect to.
      urllib3: HTTPConnectionPool url: instance of urllib3.HTTPConnectionPool

    .. code-block:: python

       from steem.http_client import HttpClient
       rpc = HttpClient(['https://steemd-node1.com', 'https://steemd-node2.com'])

    any call available to that port can be issued using the instance
    via the syntax ``rpc.exec('command', *parameters)``.

    Example:

    .. code-block:: python

       rpc.exec(
           'get_followers',
           'furion', 'abit', 'blog', 10,
           api='follow_api'
       )

    """

    def __init__(self, nodes, log_level=logging.INFO, **kwargs):
        self.return_with_args = kwargs.get('return_with_args', False)
        self.re_raise = kwargs.get('re_raise', False)
        self.max_workers = kwargs.get('max_workers', None)

        num_pools = kwargs.get('num_pools', 10)
        maxsize = kwargs.get('maxsize', 10)
        timeout = kwargs.get('timeout', 30)
        retries = kwargs.get('retries', 10)
        pool_block = kwargs.get('pool_block', False)
        tcp_keepalive = kwargs.get('tcp_keepalive', True)

        if tcp_keepalive:
            socket_options = HTTPConnection.default_socket_options + \
                             [(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1), ]
        else:
            socket_options = HTTPConnection.default_socket_options

        self.http = urllib3.poolmanager.PoolManager(
            num_pools=num_pools,
            maxsize=maxsize,
            block=pool_block,
            timeout=timeout,
            retries=retries,
            socket_options=socket_options,
            headers={'Content-Type': 'application/json'},
            cert_reqs='CERT_REQUIRED',
            ca_certs=certifi.where())
        '''
            urlopen(method, url, body=None, headers=None, retries=None,
            redirect=True, assert_same_host=True, timeout=<object object>,
            pool_timeout=None, release_conn=None, chunked=False, body_pos=None,
            **response_kw)
        '''

        self.nodes = cycle(nodes)
        self.url = ''
        self.request = None
        self.change_node()

        logger.setLevel(log_level)

    def change_node(self):
        """ Switch to the next available node.

        This method will change steembase URL of our requests.
        Use it when the current node goes down to change to a fallback node. """
        self.url = next(self.nodes)
        self.request = partial(self.http.urlopen, 'POST', self.url)

    @property
    def hostname(self):
        return urlparse(self.url).hostname

    @staticmethod
    def json_rpc_body(name, *args, api=None, as_json=True, _id=0):
        """ Build request body for steemd RPC requests.

        Args:
            name (str): Name of a method we are trying to call. (ie: `get_accounts`)
            args: A list of arguments belonging to the calling method.
            api (None, str): If api is provided (ie: `follow_api`),
             we generate a body that uses `call` method appropriately.
            as_json (bool): Should this function return json as dictionary or string.
            _id (int): This is an arbitrary number that can be used for request/response tracking in multi-threaded
             scenarios.

        Returns:
            (dict,str): If `as_json` is set to `True`, we get json formatted as a string.
            Otherwise, a Python dictionary is returned.
        """
        headers = {"jsonrpc": "2.0", "id": _id}
        if api:
            body_dict = {**headers, "method": "call", "params": [api, name, args]}
        else:
            body_dict = {**headers, "method": name, "params": args}
        if as_json:
            return json.dumps(body_dict, ensure_ascii=False).encode('utf8')
        else:
            return body_dict

    def exec(self, name, *args, api=None, re_raise=True, return_with_args=None, _ret_cnt=0):
        """ Execute a method against steemd RPC."""
        body = HttpClient.json_rpc_body(name, *args, api=api)
        try:
            response = self.request(body=body)
        except MaxRetryError as e:
            # try switching nodes before giving up
            if _ret_cnt > 2:
                time.sleep(5*_ret_cnt)
            elif _ret_cnt > 10:
                raise e
            self.change_node()
            return self.exec(name, *args,
                             re_raise=re_raise,
                             return_with_args=return_with_args,
                             _ret_cnt=_ret_cnt+1)
        except Exception as e:
            if re_raise:
                raise e
            else:
                extra = dict(err=e, request=self.request)
                logger.info('Request error', extra=extra)
                self._return(
                    response=None,
                    args=args,
                    return_with_args=return_with_args)
        else:
            if response.status not in tuple(
                    [*response.REDIRECT_STATUSES, 200]):
                logger.info('non 200 response:%s', response.status)

            return self._return(
                response=response,
                args=args,
                return_with_args=return_with_args)

    def _return(self, response=None, args=None, return_with_args=None):
        return_with_args = return_with_args or self.return_with_args

        if not response:
            result = None
        else:
            try:
                response_json = json.loads(response.data.decode('utf-8'))
            except Exception as e:
                extra = dict(response=response, request_args=args, err=e)
                logger.info('failed to load response', extra=extra)
                result = None
            else:
                if 'error' in response_json:
                    error = response_json['error']
                    error_message = error.get(
                        'detail', response_json['error']['message'])
                    raise RPCError(error_message)

                result = response_json.get('result', None)
        if return_with_args:
            return result, args
        else:
            return result

    def exec_multi(self, name, params):
        body_gen = ({
                        "method": name,
                        "params": [i],
                        "jsonrpc": "2.0",
                        "id": 0
                    } for i in params)
        for body in body_gen:
            json_body = json.dumps(body, ensure_ascii=False).encode('utf8')
            yield self._return(
                response=self.request(body=json_body),
                args=body['params'],
                return_with_args=True)

    def exec_multi_with_futures(self, name, params, max_workers=None):
        with concurrent.futures.ThreadPoolExecutor(
                max_workers=max_workers) as executor:
            # Start the load operations and mark each future with its URL
            futures = (executor.submit(self.exec, name, param)
                       for param in params)
            for future in concurrent.futures.as_completed(futures):
                yield future.result()
