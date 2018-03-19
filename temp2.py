title: "FIFA Exploratary data analysis"
Author: "Hitesh Palamada"
date: "23 April 2017"
output: html_document
---
This is an exploratory analysis of the  FIFA 2017 Player dataset, which can be 
found [here](https://www.kaggle.com/artimous/complete-fifa-2017-player-dataset-global). 

```{r}
# Importing Library
library(readr)
library(data.table)
library(sqldf)
library(dplyr)
library(radarchart)
library(tidyr)
```

Import data

```{r}
FullData <- read_csv("../input/FullData.csv")
setDT(FullData)
names(FullData)
dim(FullData)
str(FullData) 

# Unique values per column
lapply(FullData, function(x) length(unique(x))) 

```

Overall Best Club team by players rating

```{r}
#Groping players by club and appling average on players rating
TeamDF<-arrange(FullData[, list(Avg=mean(Rating)), by= "Club" ], desc(Avg) )
head(TeamDF, 10)
tail(TeamDF, 10)

#Ohh What i see, Free Agent!! which is not a team. Player who are not in club are under Free agent
#Creating new DF removing Free Agent players
FullData_RFA<- filter(FullData, !Club %in% c('Free agent'))

setDT(FullData_RFA)#changing class tot data.table

TeamDF_RFA<-arrange(FullData_RFA[, list(Avg=mean(Rating)), by= "Club" ], desc(Avg) )  

head(TeamDF_RFA, 10) # Top 10 
tail(TeamDF_RFA, 10) # Bottom 10 

```

Which continent player's are best at particular Attribute.( Example : Stamina, Ball_Control)


```{r} 
#Let's check, picking an attribute, Stamina of player. 
#Listing top 100 stamina players 
stamina_desc100<-head(arrange(FullData, desc(Stamina)), n=100)
lapply(stamina_desc100, function(x) length(unique(x))) 

unique(stamina_desc100$Nationality)

stamina_list <- stamina_desc100 %>% group_by(Nationality)  %>% tally() %>% arrange(desc(n))

stamina_list

#Lets lookin at Continent level
#Made a list of Continent_contries 
africa<-c('Algeria','Angola','Benin','Botswana','Burkina','Burundi','Cameroon','Cape Verde','Central African Republic','Chad','Comoros','Congo','Congo Democratic Republic of','Djibouti','Egypt','Equatorial Guinea','Eritrea','Ethiopia','Gabon','Gambia','Ghana','Guinea','Guinea-Bissau','Ivory Coast','Kenya','Lesotho','Liberia','Libya','Madagascar','Malawi','Mali','Mauritania','Mauritius','Morocco','Mozambique','Namibia','Niger','Nigeria','Rwanda','Sao Tome and Principe','Senegal','Seychelles','Sierra Leone','Somalia','South Africa','South Sudan','Sudan','Swaziland','Tanzania','Togo','Tunisia','Uganda','Zambia','Zimbabwe','Burkina Faso')
asia<-c('Afghanistan','Bahrain','Bangladesh','Bhutan','Brunei','Burma (Myanmar)','Cambodia','China','East Timor','India','Indonesia','Iran','Iraq','Israel','Japan','Jordan','Kazakhstan','North Korea','South Korea','Kuwait','Kyrgyzstan','Laos','Lebanon','Malaysia','Maldives','Mongolia','Nepal','Oman','Pakistan','Philippines','Qatar','Russian Federation','Saudi Arabia','Singapore','Sri Lanka','Syria','Tajikistan','Thailand','Turkey','Turkmenistan','United Arab Emirates','Uzbekistan','Vietnam','Yemen','Russia')
europe<-c('Albania','Andorra','Armenia','Austria','Azerbaijan','Belarus','Belgium','Bosnia and Herzegovina','Bulgaria','Croatia','Cyprus','Czech Republic','Denmark','Estonia','Finland','France','Georgia','Germany','Greece','Hungary','Iceland','Ireland','Italy','Latvia','Liechtenstein','Lithuania','Luxembourg','Macedonia','Malta','Moldova','Monaco','Montenegro','Netherlands','Norway','Poland','Portugal','Romania','San Marino','Serbi','Slovakia','Slovenia','Spain','Sweden','Switzerland','Ukraine','England','Vatican City','Republic of Ireland','Wales')
north_america<-c('Antigua and Barbuda','Bahamas','Barbados','Belize','Canada','Costa Rica','Cuba','Dominica','Dominican Republic','El Salvador','Grenada','Guatemala','Haiti','Honduras','Jamaica','Mexico','Nicaragua','Panama','Saint Kitts and Nevis','Saint Lucia','Saint Vincent and the Grenadines','Trinidad and Tobago','United States')
oceania<-c('Australia','Fiji','Kiribati','Marshall Islands','Micronesia','Nauru','New Zealand','Palau','Papua New Guinea','Samoa','Solomon Islands','Tonga','Tuvalu','Vanuatu')
south_america<-c('Argentina','Bolivia','Brazil','Chile','Colombia','Ecuador','Guyana','Paraguay','Peru','Suriname','Uruguay','Venezuela')

# chainging country by continent
stamina_list$Nationality[stamina_list$Nationality %in% africa] <- "africa"
stamina_list$Nationality[stamina_list$Nationality %in% asia] <- "asia"
stamina_list$Nationality[stamina_list$Nationality %in% europe] <- "europe"
stamina_list$Nationality[stamina_list$Nationality %in% north_america] <- "north_america"
stamina_list$Nationality[stamina_list$Nationality %in% oceania]<-"oceania"
stamina_list$Nationality[stamina_list$Nationality %in% south_america]<-"south_america"

unique(stamina_list$Nationality) # Check for nationality values

stamina_list <- stamina_list %>% group_by(Nationality)

stamina_list
```

Best players, and Which Attribute which player has to develop


```{r} 
#Most intresting  part which I love,learning and imporving !!

# Making a subset with selective attributes. 

FullData_Subset <- subset(FullData, select = c("Name" ,"Nationality", "Rating", "Preffered_Position", "Ball_Control", "Dribbling", "Marking","Sliding_Tackle", "Standing_Tackle", "Aggression", "Reactions", "Attacking_Position", "Crossing", "Acceleration", "Balance" ))

FullData_Subset$Preffered_Position <- gsub("/*", "", FullData_Subset$Preffered_Position )

unique(FullData_Subset$Preffered_Position)

#Chaning postions into  - Forward , Midfielder, Defender , Goalkeeper
FullData_Subset$Preffered_Position <- gsub(".*W", "Forward", FullData_Subset$Preffered_Position )
FullData_Subset$Preffered_Position <- gsub("Forward*.", "Forward", FullData_Subset$Preffered_Position )
FullData_Subset$Preffered_Position <- gsub("GK", "Goalkeeper", FullData_Subset$Preffered_Position )
FullData_Subset$Preffered_Position <- gsub(".*B", "Defender", FullData_Subset$Preffered_Position )
FullData_Subset$Preffered_Position <- gsub("Defender*.", "Defender", FullData_Subset$Preffered_Position )
FullData_Subset$Preffered_Position <- gsub(".*M", "Midfielder", FullData_Subset$Preffered_Position )
FullData_Subset$Preffered_Position <- gsub("Midfielder*.", "Midfielder", FullData_Subset$Preffered_Position)
FullData_Subset$Preffered_Position <- gsub("STCF", "Forward", FullData_Subset$Preffered_Position )                                 
FullData_Subset$Preffered_Position <- gsub("ST", "Forward", FullData_Subset$Preffered_Position )                                 
FullData_Subset$Preffered_Position <- gsub("CF", "Forward", FullData_Subset$Preffered_Position )                                 
FullData_Subset$Preffered_Position <- gsub("CFST", "Forward", FullData_Subset$Preffered_Position )                                 

unique(FullData_Subset$Preffered_Position)
#Run it twice_thrice any number of times, if positions are not converted into  - Forward , Midfielder, Defender , Goalkeeper

FullData_Subset

```	


```{r} 
#Best player  at positions - Forward , Midfielder, Defender , Goalkeeper
sqldf("Select name ,Nationality,max(Rating) as max, Preffered_Position from FullData_Subset group by Preffered_Position ")
```


```{r} 
# Creating seperate data frames for Forward , Midfielder, Defender , Goalkeeper players 

ForwardDF<- FullData_Subset%>% filter(FullData_Subset$Preffered_Position =="Forward")
MidfielderDF<- FullData_Subset%>% filter(FullData_Subset$Preffered_Position =="Midfielder")
DefenderDF<- FullData_Subset%>% filter(FullData_Subset$Preffered_Position =="Defender")
GoalkeeperDF<- FullData_Subset%>% filter(FullData_Subset$Preffered_Position =="Goalkeeper")

#Picking up Forward players data frame, Which Attribute which player has to develop.! 
#Considering players skill below  95 percentile has to be improved, makring player Attributes development as "Yes"
#Time being am selecting few Attribute.

Ball_Controldf <-data.frame(ifelse(ForwardDF$Ball_Control >= quantile(ForwardDF$Ball_Control, .95) , "No" , "Yes") )
Dribblingdf <-data.frame(ifelse(ForwardDF$Dribbling >= quantile(ForwardDF$Dribbling, .95) , "No" , "Yes") )
Markingdf <-data.frame(ifelse(ForwardDF$Marking >= quantile(ForwardDF$Marking, .95) , "No" , "Yes") )
Sliding_Tackledf <-data.frame(ifelse(ForwardDF$Sliding_Tackle >= quantile(ForwardDF$Sliding_Tackle, .95) , "No" , "Yes") )
Standing_Tackledf <-data.frame(ifelse(ForwardDF$Standing_Tackle >= quantile(ForwardDF$Standing_Tackle, .95) , "No" , "Yes") )
Aggressiondf <-data.frame(ifelse(ForwardDF$Aggression >= quantile(ForwardDF$Aggression, .95) , "No" , "Yes") )
Reactionsdf <-data.frame(ifelse(ForwardDF$Reactions >= quantile(ForwardDF$Reactions, .95) , "No" , "Yes") )
Attacking_Positiondf <-data.frame(ifelse(ForwardDF$Attacking_Position >= quantile(ForwardDF$Attacking_Position, .95) , "No" , "Yes") )
Crossingdf <-data.frame(ifelse(ForwardDF$Crossing >= quantile(ForwardDF$Crossing, .95) , "No" , "Yes") )
Accelerationdf <-data.frame(ifelse(ForwardDF$Acceleration >= quantile(ForwardDF$Acceleration, .95) , "No" , "Yes") )
Balancedf <-data.frame(ifelse(ForwardDF$Balance >= quantile(ForwardDF$Balance, .95) , "No" , "Yes") )

# Changing column names

colnames(Ball_Controldf) <- c("Ball_Control")
colnames(Dribblingdf) <- c("Dribbling")
colnames(Markingdf) <- c("Marking")
colnames(Sliding_Tackledf) <- c("Sliding_Tackle")
colnames(Standing_Tackledf) <- c("Standing_Tackle")
colnames(Aggressiondf) <- c("Aggression")
colnames(Reactionsdf) <- c("Reactions")
colnames(Attacking_Positiondf) <- c("Attacking_Position")
colnames(Crossingdf) <- c("Crossing")
colnames(Accelerationdf) <- c("Acceleration")
colnames(Balancedf) <- c("Balance")

attributes_to_develop<-cbind(ForwardDF$Name,Ball_Controldf, Dribblingdf, Markingdf,Sliding_Tackledf, Standing_Tackledf, Aggressiondf, Reactionsdf, Attacking_Positiondf, Crossingdf, Accelerationdf, Balancedf )

write.csv(attributes_to_develop, file = 'attributes_to_develop_Forwardplayers.csv', row.names = F)

```
Radar chart

```{r} 
#complete profile of individual players I create a radar chart

library(radarchart)
library(tidyr)
#Selecting top players by rating from data
top20 <- head(FullData, 20)

radarDF <- top20 %>% select(Name, 18:53) %>% as.data.frame()

radarDF <- gather(radarDF, key=Label, value=Score, -Name) %>%
  spread(key=Name, value=Score)

chartJSRadar(scores = radarDF, maxScale = 100, showToolTipLabel = TRUE)
```
That's all for now. Thanks for reading. If you have any feedback, I'd love to hear! I appreciate all the feedback I've received so far.
