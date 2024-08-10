import json
from pydantic import BaseModel

class BaseValidate(BaseModel):
    def validate(self):
        return True

class Date4Bytes(BaseValidate):
    day: int = 31
    month: int = 12
    year: int = 2021

    def validate(self):
        data_dict = json.loads(self.model_dump_json())
        # print(data_dict)

        if int(data_dict["day"]) > 31 or int(data_dict["day"]) < 1:
            raise ValueError("Day must be between 1 and 31 got {0}".format(data_dict['day']))
        if int(data_dict["month"]) > 12 or int(data_dict["month"]) < 1:
            raise ValueError("Month must be between 1 and 12 got {0}".format(data_dict['month']))
        if int(data_dict["year"]) > 9999 and int(data_dict["year"]) < 1:
            raise ValueError("Year must be between 1 and 9999 got {0}".format(data_dict['year']))
        
        return True

class EnumStatus:
    SUCCESS = "Success"
    ERROR = "Error"

def make_response(message: str, data: any, status: str):
    return {
        "message": message,
        "data": data,
        "status": status
    }

def make_response_auto_catch(lamda_call: callable):
    try:
        return make_response("ok", lamda_call(), EnumStatus.SUCCESS)
    except Exception as e:
        return make_response(f"Args: {e.args}\nMsg: {e}", None, EnumStatus.ERROR)