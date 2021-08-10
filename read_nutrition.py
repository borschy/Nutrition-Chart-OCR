import os
from paddleocr import PaddleOCR

class Reader:
    def __init__(self, language="ch"):
        self.ocr = PaddleOCR(lang=language)
    
    def read_img(self, img_path:str):
        result = self.ocr.ocr(img_path)
        result = [line[1][0] for line in result]
        return result
    
    def parse_results(self, result:list):
        nutrition = {}
        for idx, elem in enumerate(result):
            if elem in ["能量", "蛋白质", "脂肪", "碳水化合物", "膳食纤维", "钠"]:
                nutrition[elem] = result[idx+1]
        return nutrition

    def read_single(self, img_path:str):
        results = self.read_img(img_path)
        nutrition_dict = self.parse_results(results)
        return nutrition_dict

    def read_folder(self, folder_path:str):
        all_files = []
        files = [os.path.join(folder_path, name) for name in os.listdir(folder_path) 
                    if os.path.splitext(name)[1] in [".jpg", ".jpeg", ".png"]]
        for file in files:
            info = {}
            info["name"] = file
            info["nutrition"] = self.read_single(file)
            all_files.append(info)
        return all_files

    

if __name__ == "__main__":
    r = Reader()
    info = r.read_folder(r"F:\\data\\nutrition")
    print(info)