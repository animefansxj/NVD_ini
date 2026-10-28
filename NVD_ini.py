#################################################
# NowVideo Ini file operation Class & Functions #
#            by af_xj@hotmail.com               #
#                Rev 20261028A                  #
#            (C) 25' 26' NowVideo               #
#             Default License: MIT              #
#  -------------------------------------------  #
#  If this source code is subject to a          #
#  separately negotiated license agreement,     #
#  copies of the source code shall be governed  #
#  by the terms of that agreement. Otherwise,   #
#  it shall be licensed under the default       #
#  agreement set forth above.                   #
#################################################


import re
import sys
import traceback

class Section:
    Name: str
    Items: list[dict]
    Comment: str|None

    def __init__(self,Name:str,Comment:str|None=None):
        self.Name = Name
        self.Items = [dict]
        self.Comment = Comment

class Config:
    __Path: str
    __Loaded:bool
    __Sections: list[Section]
    __Context: list[str]

    def __init__(self):
        self.__Sections = []

    def ReadIni(self,Path):
        HasFirstSections = False
        self.__Path = Path
        try:
            File = open(Path,"rt")
            self.__Context = File.readlines()
            if(len(self.__Context) < 1):
                self.__Loaded = False
                print(f"[X] | Conf file {Path} is empty.")
                return

            for line in self.__Context:
                if(not line.startswith("#")):
                    if(re.match(r"^\[\w+\]",line)):
                        self.__Sections.append(Section(line[1:-2]))
                        if(not HasFirstSections):
                            HasFirstSections = True
                    if(re.search(r"\s*[\w\-_]+\s*=\s*[\w\{\}\-\[\]_,]+\s*",line)):
                        if(HasFirstSections):
                            Key = re.findall(r"^\s*([\w\-_]+)",line)[0]
                            Value = re.findall(r"=\s*([\w\{\}\-\[\]_,]+)",line)[0]
                            if(re.match(r"#[\w\-_,]+",line)):
                                Comment = re.findall(r"#([\w\-_,]+)",line)[0]
                            else:
                                Comment = None
                            self.__Sections[len(self.__Sections)-1].Items.append({'Key':Key,'Value':Value,'Comment':Comment})

            File.close()

            if(HasFirstSections and (len(self.__Sections[0].Items) > 0)):
                self.__Loaded = True
            else:
                self.__Loaded = False
        except Exception as e:
            self.__Loaded = False
            Lib,LineNo,FuncName,Stnax = traceback.extract_tb(sys.exc_info()[2])[-1]
            print(f"[X] | Could not load conf from file: {self.__Path}.\n    |\t{e}\n    |\t{Lib}::{FuncName} ,Line {LineNo}: {Stnax}")


    def isOK(self) -> bool:
        return self.__Loaded

    def GetSectionIndex(self,SectionName:str) -> int:
        if(self.__Loaded):
            Index = 0
            for Section in self.__Sections:
                if(Section.Name == SectionName):
                    return Index
                else:
                    Index += 1
            return -1
        else:
            return -1

    def GetKeyIndex(self,SectionName:str,KeyName:str) -> int:
        if(self.__Loaded):
            sIndex = self.GetSectionIndex(SectionName)
            if(sIndex >= 0):
                kIndex = 0
                for Item in self.__Sections[sIndex].Items:
                    if(Item['Key'] == KeyName):
                        return kIndex
                    else:
                        kIndex += 1
                return -1
            else:
                return -1
        else:
            return -1


    def hasSection(self,SectionName:str) -> bool:
        if(self.__Loaded):
            if(self.GetSectionIndex(SectionName) >= 0):
                return True
            else:
                return False
        else:
            return False

    def hasKey(self,SectionName:str,KeyName:str) -> bool:
        if(self.__Loaded):
            if(self.GetKeyIndex(SectionName,KeyName)):
                return True
            else:
                return False
        else:
            return False

    def GetValue(self,SectionName:str,KeyName:str) -> str|None:
        if(self.__Loaded):
            SectionIndex = self.GetSectionIndex(SectionName)
            if(SectionIndex < 0):
                return None
            else:
                KeyIndex = self.GetKeyIndex(SectionName,KeyName)
                if(KeyIndex < 0):
                    return None
                else:
                    return self.__Sections[SectionIndex].Items[KeyIndex]['Value']
        else:
            return None
    
    def GetValueA(self,SectionName:str,KeyName:str,AltValue:str) -> str:
        Value = self.GetValue(SectionName,KeyName)
        if(Value):
            return Value
        else:
            return AltValue

    def Rush(self) -> None:
        print("[i] | Start rush the conf.")
        if(self.__Loaded):
            for Section in self.__Sections:
                for Item in Section.Items:
                    print(f"    |\t @{Section.Name}\t::\t {Item['Key']}: {Item['Value']}")
        else:
            print("[X] | Conf not loaded.")
