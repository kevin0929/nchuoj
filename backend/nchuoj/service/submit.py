import base64
import requests


class SubmitService:
    def __init__(self):
        self.JUDGE0_BASE_API_URL = "http://140.120.31.174:2358"


    def encode_base64(self, data: str) -> str:
        '''for url parameter base64_encoded=true
        '''
        return base64.b64encode(data.encode("utf-8")).decode("utf-8")

    def submit(
        self,
        langid: int,
        source_code: str,
        memory_limit: float,
        cpu_time_limit: float,
        testcases,
        wait: bool = True
    ):
        '''
            1. iterative make payload
            2. send request to judge0 api
            3. wait judge0 execute completely, receive response and query result
            4. decode result and return to problem_api
        '''
        execute_time = 0.0
        memory_usage = 0
        final_status = "Accepted"

        JUDGE0_API_URL = f"{self.JUDGE0_BASE_API_URL}/submissions?base64_encoded=true&wait=true" if wait else f"{self.JUDGE0_BASE_API_URL}/submissions"

        for testcase in testcases:
            stdin = self.encode_base64(testcase["input_data"].decode("utf-8"))
            expected_output = self.encode_base64(testcase["output_data"].decode("utf-8"))

            payload = {
                "source_code": self.encode_base64(source_code),
                "language_id": langid,
                "memory_limit": memory_limit,
                "cpu_time_limit": cpu_time_limit,
                "stdin": stdin,
                "expected_output": expected_output
            }

            response = requests.post(JUDGE0_API_URL, json=payload)
 
            if response.status_code == 201:
                result = response.json()
                status = result["status"]["description"]

                # if test failure, stop continuously test
                if status != "Accepted":
                    final_status = status
                    break

                # sum up time and memory of all testcase
                execute_time += float(result["time"])
                memory_usage += int(result["memory"]) 

        resp = {
            "execute_time": execute_time,
            "memory_usage": memory_usage,
            "status": final_status
        }

        return resp

    
    def get_language_id(self, language_name: str) -> int:
        language_table = {
            "C": 50,
            "C++": 54,
            "Python": 71,
        }

        return language_table[language_name]
