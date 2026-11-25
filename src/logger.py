import requests
import json
from datetime import datetime
import time
import logging
import sys

logger = logging.getLogger("LoggedSession")
logger.setLevel(logging.INFO)
logger.handlers.clear()
console = logging.StreamHandler(sys.stdout)
console.setLevel(logging.INFO)
console.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(console)

class LoggedSession(requests.Session):
    def request(self, method, url, **kwargs):
        start_time = time.time()
        response = super().request(method, url, **kwargs, verify=False)
        elapsed = round((time.time() - start_time), 2)

        log = {
            "timestamp": datetime.now().isoformat(),
            "request": {
                "method": method,
                "url": url,
                "params": kwargs.get("params"),
                "data": kwargs.get("data"),
                "json": kwargs.get("json"),
            },
            "response": {
                "status_code": response.status_code,
                "body": self._safe_response_body(response),
            },
            "elapsed_time": f"{elapsed} segundos",
        }

        logger.info(json.dumps(log, ensure_ascii=False))
        return response

    def _safe_response_body(self, response, max_size=2000):
        try:
            body = response.text
            if len(body) > max_size:
                return body[:max_size] + "...(truncado)"
            return body
        except Exception:
            return "<não foi possível ler o body>"

    def _mask_headers(self, headers):
        if not headers:
            return headers
        headers = headers.copy()
        if "Authorization" in headers:
            headers["Authorization"] = "***"
        return headers