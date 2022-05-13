from logging import warning
import numpy as np;import pandas as pd
import NeuralNetwork

x_test = np.genfromtxt('x_test.csv', delimiter=',')

#initialization
network = NeuralNetwork.Modifiable_NN([x_test.shape[0],20,20,1],activations={1:'relu',2:'relu',3:'relu',4:'relu'},cost_function='mse',param_init_type='xavier')


#Getting the data for entire country  based on one dataset
rayon = ["Qəbələ" ,"Bakı","Gəncə","Naxçıvan","Xankəndi","Lənkəran","Mingəçevir","Naftalan","Sumqayıt","Şəki","Şirvan","Yevlax","Abşeron"  ,"Ağcabədi" ,"Ağdam" ,"Ağdaş" ,'Ağstafa' ,'Ağsu' ,"Astara" 
"Babək","Balakən","Beyləqan" ,"Bərdə" ,"Biləsuvar" ,"Cəbrayıl" ,"Cəlilabad" ,"Culfa" ,"Daşkəsən" ,"Füzuli" ,"Gədəbəy" ,"Goranboy" ,"Göyçay" ,"Göygöl" ,"Hacıqabul" ,"Xaçmaz" ,"Xızı" ,"Xocalı" ,
"Xocavənd" ,"İmişli" ,"İsmayıllı" ,"Kəlbəcər" ,"Kəngərli" ,"Kürdəmir" ,"Qax" ,"Qazax" ,"Qobustan" ,"Quba" ,"Qubadlı" ,"Qusar" ,"Laçın" ,"Lerik" ,"Lənkəran" ,"Masallı" ,"Neftçala" 
"Oğuz" ,"Ordubad" ,"Saatlı" ,"Sabirabad" ,"Salyan" ,"Samux" ,"Sədərək" ,"Siyəzən" ,"Şabran" ,"Şahbuz" ,"Şamaxı" ,"Şəki" ,"Şəmkir" ,"Şərur" ,"Şuşa" ,"Tərtər" ,"Tovuz" ,"Ucar" ,"Yardımlı" 
"Yevlax" ,"Zaqatala" ,"Zəngilan" ,"Zərdab"]


#Labels that will be shown in UI
height_of_river_today = []
general_average_h_for_this_season = []
rain_flow_next_week = []
rain_flow_second_week = []
predicted_max_for_third_week = []
max_height_limit = []
flood_prob_l = []

#Compute Probability of flood
def flood_prob(max_h,predicted):
    prob = predicted/max_h
    if prob > 1:  prob = 1
    return prob*100

       
#We are adding 1 warning case for Qebele region and test whether it works or not 

warning_case = np.array([2.1 , 2 , 4 , 3])

#warning_case = warning_case.reshape(4,1)      
print(x_test[:,0])  
#x_test[:,0] = x_test[:,0].reshape(4,1)
x_test[:,0] = warning_case

for i in range(len(rayon)):

    now_data = x_test[:,i].reshape(4,1)
    height_of_river_today.append(now_data[0])
    general_average_h_for_this_season.append(now_data[1])
    rain_flow_next_week.append(now_data[2])
    rain_flow_second_week.append(now_data[3])

    predicted = network.predict(now_data)
    predicted = predicted[0][0]
    
    predicted_max_for_third_week.append(predicted)
    max_height_limit.append(2.3) # We have one dateset corresponds to only 1 river but we assume that we have the data of all river thats why we just give 1 max height
    
    #print('max height',max_height_limit[-1])
    cond_and_risk = flood_prob(max_height_limit[-1],predicted)
    flood_prob_l.append( cond_and_risk )





data = []
for i in range(len(rayon)):
    data.append({'Rayon_adlari':rayon[i],'height_of_river_today':height_of_river_today[i],'general_average_h_for_this_season':general_average_h_for_this_season[i],
        'rain_flow_next_week':rain_flow_next_week[i],'rain_flow_second_week':rain_flow_second_week[i],'predicted_max_for_third_week':predicted_max_for_third_week[i],
        'max_height_limit':max_height_limit[i],'flood_prob':flood_prob_l[i]}
    ) 
    

data_df = pd.DataFrame(data) 
data_df.to_excel('Auye_data.xlsx')
