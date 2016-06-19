
LINKS
https://azure.microsoft.com/en-us/documentation/articles/machine-learning-recommendation-api-documentation/

--------------------------------
(1) Catalog
--------------------------------
https://azure.microsoft.com/en-us/documentation/articles/machine-learning-recommendation-api-documentation/#8-catalog

Without features - <Item Id>,<Item Name>,<Item Category>[,<Description>]
With features    - <Item Id>,<Item Name>,<Item Category>,[<Description>],<Features list>



--------------------------------
(2) Usage
--------------------------------
https://azure.microsoft.com/en-us/documentation/articles/machine-learning-recommendation-api-documentation/#9-usage-data

<User Id>,<Item Id>[,<Time>,<Event>]


TIME format: YYYY/MM/DDTHH:MM:SS 
    ex.  2013/06/20T10:00:00
Event:
    -Click
    -RecommendationClick
    -AddShopCart
    -RemoveShopCart
    -Purchase


--------------------------------
(3) Build
--------------------------------
http://recommendations.azurewebsites.net/

my account:
address:    yoichi.kawasaki@hotmail.co.jp
primarykey: 5rAttaxuWkAAR29zkOyAUBdo/2nJEL0SD11hmagPJu8

project: decode2016
http://recommendations.azurewebsites.net/#/projects/decode2016




----------------------------------
RecoAPIがサポートする3つのシナリオ
----------------------------------
- Frequently Bought Together (FBT) Recommendations
- Item to Item Recommendations
- Customer to Item Recommendations

