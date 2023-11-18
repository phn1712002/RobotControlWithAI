import numpy as np
from vietnam_number import w2n
from underthesea import text_normalize
from .Data import direction_maps, command_accept_maps, ner_label_skip, ner_type_maps, string_maps, key_pm, key_dir

def getNumberAngleFromText(text_array:tuple, ner_array:tuple):
    index = np.where(ner_array == key_pm)
    if not index is None:
        format_str = str(text_array[index]).lower()
        number_angle = w2n(format_str)
        return number_angle
    else: return None

def getDirMotorFromText(text_array:tuple, ner_array:tuple):
    index = np.where(ner_array == key_dir)
    if not index is None:
        format_str = str(text_array[index]).lower()
        return direction_maps[format_str]
    return None 

def checkCommandAccept(string_ner:str):
    string_ner = string_ner.lower()
    if string_ner in command_accept_maps: return (True, command_accept_maps[string_ner])
    return (False, None)

def fixTextVietnamese(text:str):
    return text_normalize(text)

def getNameObjFromText(text_array:tuple, ner_array:tuple):
    pass

def getDirAndStrOfNER(ouput_ner:list):
        grouped_data_str = []
        grouped_data_tag = []
        save_grouped_data = False
        
        begin_text = False
        tag_last = None
        
        for word, label in ouput_ner:
            
            if save_grouped_data:
                grouped_data_str.append(fullStr)
                grouped_data_tag.append(tag)
                begin_text = False
                
            tag = label.split('-')
            type_tag = tag[0]
            name_tag = tag[len(tag) - 1]
            
            if tag_last != name_tag: 
                tag_last = name_tag
                fullStr = None
                
            if not begin_text: fullStr = None 
            
            if name_tag not in ner_label_skip:
                if type_tag in ner_type_maps:
                    if ner_type_maps[type_tag] == 0: 
                        fullStr = string_maps['none'] + word
                        begin_text = True
                    elif ner_type_maps[type_tag] == 1: 
                        if not fullStr is None: 
                            fullStr += string_maps['space'] + word
                    elif  ner_type_maps[type_tag] == 2: 
                        if not fullStr is None: 
                            fullStr += string_maps['space'] + word
                            save_grouped_data = True
            
            
            return grouped_data_str, grouped_data_tag

            