Title: DSS Final Report  
Author: 建文 蘇

# Abstract #

摘要
一般信貸申請案件經過銀行審核篩選後可以順利申請到貸款的往往只有初始申請者總人數的三成， 通過率相當的低，因此網路小額信貸逐步興起，開始打破傳統融資模式。
我們想藉由分析風險因素來提供一分風險評估報告，我們的系統設計採用了八個步驟來設計與建構模型，以提升資料完整度與準確性。使用的資料來源為Kaggle的開放資料集以及Lending Club開放的API，挑出其中關連性較高的欄位，預計使用這個資料集訓練出一個能夠預測借款分級的分類模型。
希望能夠提供一個媒合以及評估的平台，將金錢借貸給被銀行拒絕的貸款弱勢族群及需要小額借貸的用戶，並藉由此平台找出需要借款的人以及希望投資的人。


----

# Main Part #

----

## Steps and Approach ##

----

# Demo #

----

## Ｍodels ##

	我們測試了多種不同的Model來比較其分類的準確度，透過測試多種不同的模型可以更加了解我們資料的相性。

	如下表所示，我們整理了各個模型的準確度，最後我們選擇了最具效率的模型 — Decision Tree。Decision Tree的準確度相當高且模型訓練的時間相較於SVM與KNN少了許多。

| Model | Accuracy | Int_rate | Grade/Sub |
| :-----: | :-----: | :-----: | :-----: |
| Decision Tree | 0.0489 | X | Sub Grade |
| Decision Tree | 0.8622 | ✓ | Sub Grade |
| Decision Tree | 0.9540 | ✓ | Grade |
| Decision Tree | 0.2562 | X | Grade |
| SVM | Run Over 8 hrs | - | - |
| KNN | 0.66 (About 2 hrs) | ✓ | Grade |
| Logistic Regression |  | ✓ | Grade |

----

## APIs ##

 	我們採用Keras來實作我們的模型。首先，我們使用Pandas將資料集(這裡使用csv)讀入，並檢查其有沒有空值的欄位。我們發現資料來源有74個column，但是實際提供有效資料的欄位僅有35個，因此在一開始我們就剔除了39個欄位。
	由於要讓網頁能夠將使用者輸入的資料傳入模型進行預測，因此我們以Node.js架設了REST API。這個API能夠將使用者的輸入值傳入python script，並將預測結果回傳給網頁。為了能夠在公開的網域上Demo以及安全性上的考量，最後採用了Azure的ML服務架設了Python的Train與Predict API，並搭配了GCP的Google Function做出帶有SSL加密的REST API。


----

## Web Page ##

----

## Source Code ##

	原始碼	
	以下包含了各Model的Source Code，主要包含SVM, KNN, Decision Tree, MLP。建置的環境皆為Anaconda的python 3.6.5，並需額外安裝Keras與TensorFlow套件。除了訓練用的原始碼外，也提供預測的原始碼，以方便建構成預測的API。


* SVM: 
* KNN: 
* MLP:
* Decision Tree: https://github.com/johnny12150/DSS_P2P/blob/master/notebook/DecisionTree.py
* Logistic Regression: https://github.com/johnny12150/DSS_P2P/blob/master/notebook/LogisticRegression.py
* Train: https://github.com/johnny12150/DSS_P2P/blob/master/notebook/train.py
* Predict: https://github.com/johnny12150/DSS_P2P/blob/master/notebook/predict.py
* Visualise data: https://github.com/johnny12150/DSS_P2P/blob/master/notebook/Grade%20-%20MLP.ipynb
