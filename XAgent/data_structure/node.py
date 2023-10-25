import os
import abc
from copy import deepcopy
from enum import Enum
from typing import List
from dataclasses import dataclass

from XAgent.message_history import MessageHistory
from XAgent.utils import ToolCallStatusCode, TaskStatusCode



class Node(metaclass = abc.ABCMeta):
    def __init__(self):
        pass

class ToolType(Enum):
    Default = 'Default'
    BuiltIn = 'BuildIn'
    ToolServer = 'ToolServer'
    Rapid = 'Rapid'
    N8N = 'N8N'
    Custom = 'Custom'
    def __hash__(self):
        return hash(self.value)
        

class ToolNode(Node):
    def __init__(self,data:dict = None,tool_type=ToolType.Default):
        self.tool_type = tool_type
        self.father: ToolNode = None
        self.children: list[ToolNode] = []

        self.expand_num = 0
        if data is not None:
            self.data = data 
        else:
            self.data = {
                "content": "",
                "thoughts": {
                    "properties": {
                        "thought": "",
                        "reasoning": "",
                        "plan": "",
                        "criticism": "",
                    },
                },
                "command": {
                    "properties": {
                        "name": "",
                        "args": "",
                    },
                },
                "tool_output": "",
                "tool_status_code": ToolCallStatusCode.TOOL_CALL_SUCCESS,
            }
        self.history: MessageHistory = MessageHistory()

    @property
    def content(self):
        return self.data["content"]
    
    @property
    def thought(self):
        if self.data["thoughts"]["properties"].get('thought','') == "":
            return None
        return self.data["thoughts"]["properties"]["thought"]
    
    @property
    def reasoning(self):
        if self.data["thoughts"]["properties"].get('reasoning','') == "":
            return None
        return self.data["thoughts"]["properties"]["reasoning"]
    
    @property
    def plan(self):
        if self.data["thoughts"]["properties"].get('plan','')== "":
            return None
        return self.data["thoughts"]["properties"]["plan"]
    
    @property
    def criticism(self):
        if self.data["thoughts"]["properties"].get("criticism",'') == "":
            return None
        return self.data["thoughts"]["properties"]["criticism"]
    
    @property
    def tool_name(self):
        if self.data["command"]["properties"]["name"] == "":
            return None
        return self.data["command"]["properties"]["name"]
    @property
    def tool_args(self):
        if self.data["command"]["properties"]["args"] == "":
            return None
        return self.data["command"]["properties"]["args"]


    @property
    def process(self):
        data = []
        now_node = self
        while now_node.father != None:
            data = [now_node.data] + data
            now_node = now_node.father
        return data

    def to_json(self):
        data = deepcopy(self.data)
        data["tool_status_code"] = data["tool_status_code"].name
        return data

    def get_depth(self):
        if self.father == None:
            return 0
        return self.father.get_depth() + 1
    
    def get_subtree_size(self):
        if self.children == []:
            return 1
        now_size = 1
        for child in self.children:
            now_size += child.get_subtree_size()
        return now_size



