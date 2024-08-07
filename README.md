this is a for learn project,this is my frist time make a project on the github and my english is not really good hope today can be dayone.

in this project I use python to code just use a some base skill
I use YOLO moudel V3 in this project just and secard and three file's
just for a basic use if you feel my project is useful I will very happy ;-;

okay let start it.

2024/08/06
# 影像辨識
這是我的第一個記錄起來的學習專案，也從今天我真真正正的踏上了程式這一條路。

首先來確認此次學習的目標，我採用top to down的學習方式由於這是我第一次接觸openCV，所以我決定先做出一個具有影像辨識功能的程式再來加以改進、修正，由上至下的來實作。

這次完成的目標:
    1.先製作出能夠進行基礎影像辨識的軟體
    2.我預計將程式設計成能夠辨識車子、卡車、摩托車等以利用於行車影像辨識及預警的領域
    3.盡可能熟練openCV這個模組的運用方法
    4.試著以物件導向的邏輯來開發程式
    5.初步的了解影像辨識的原理
    
首先我使用chatGPT來生成了一個開發的框架以及步驟
![image](https://hackmd.io/_uploads/SkjZ6a0tA.png)

由於此次只是做一個初步的學習，並且數據的收集、處理，網路上有現成的數據，並且已經有一定良率的訓練以及優化了，本次的學習重點是軟體開發，所以將著重於軟體的部分。
(其實就是GPT說了9句廢話1句有用的話)

# 關於模型選擇
GPT提到需要選擇一個學習模型、並且預設了YOLO，所以我選擇YOLO作為此次開發的模型
我在hackMD上找到一篇[小論文](https://hackmd.io/@allen108108/r1-wSTAjS)，是關於YOLO一定程度上的原理解釋說得非常詳細。

我著重看的是YOLO的限制，文中提到:
「YOLO 在邊界框預測上有很強的空間限制，因為每一個網格僅能預測兩個單一目標的邊界框。這樣的空間限制，限制了 YOLO 對相鄰目標的預測。換句話說，YOLO 對於成群聚集的小物件 ( 例如鳥群 ) 有著預測上的困難。」

由於應用的領域是識別人類、車輛、標幟標線，所以這個限制並沒有多大的影響，以及fastYOLO可以達到每秒100多偵的影像辨識，非常適用於行車安全的領域。

我大概想做成這種效果，應該會想加上nametag之類的東西
![30937-1](https://hackmd.io/_uploads/H14WMZJ5A.jpg)

# 開發與思路紀錄
一開始我想先將所有的檔案路徑和一些變量的定義完成，這部分通常沒有太大的問題。
已經讀取影片、YOLO的數據，我使用Print檢測後都能夠讀取到，接下來困難的就是要開始研究YOLO的實現的方法了。

然後就是一個初步的思路:

![image](https://hackmd.io/_uploads/r1TVs-Jq0.png)


首先要搞定的第一步就是影像讀取，使用openCV提取影像、使用YOLO辨識，然後利用YOLO返還的函數取得位置，之後畫線就搞定了。

第一步完成了影像的提取，需要逐禎去分析，以小論文上建了使用
```
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(self.classes[class_ids[i]])
                color = self.colors[class_ids[i]]
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                print(f"Detected {label} with confidence {confidences[i]:.2f} at [{x}, {y}, {w}, {h}]")  # Debug message
```

> 看起來似乎有點混亂，不過沒關係我會在最後對代碼做一個重構。

主程式大概這樣就完成了基本的功能，把一些顏色、影片逐貞提取等等，再來透過openCV取得了物件的位置後，添加線就random一下顏色，就完成了基本的功能。

目前看起來像是這樣:
![image (1)](https://hackmd.io/_uploads/SkkGhrxcR.png)

