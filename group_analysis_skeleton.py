#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scene-cat problem set for PSY 1210 - Fall 2018

@author: Michael Mack
"""

#%% import block 
import numpy as np
import scipy as sp
import scipy.stats
import os
import shutil


#%%
# copy files from testing room folders to raw data, rename files to include
# testing room letter in the filename

# find and copy important_file.txt from directory1 to directory2
#filepath = os.path.join('directory1','important_file.txt')
#newpath = os.path.join('directory2','important_file.txt')
#shutil.copyfile(filepath,newpath)
testingrooms = ['A','B','C']
for room in testingrooms:
    path="/Users/asamson/Documents/GitHub/ps2-nosmasa/"+"testingroom"+ room +"/experiment_data.csv"
    newpath="/Users/asamson/Documents/GitHub/ps2-nosmasa/"+"rawdata/"+"experiemtn_data_"+ room +".csv"
    shutil.copyfile(path,newpath)


#%%
# read in all the data files in rawdata directory using a for loop
# columns: subject, stimulus, pairing, accuracy, median RT
#
data = np.empty((0,5))
for room in testingrooms:
    newpath="/Users/asamson/Documents/GitHub/ps2-nosmasa/"+"rawdata/"+"experiemtn_data_"+ room +".csv"
    tmp = sp.loadtxt(newpath,delimiter=',')
    data = np.vstack([data,tmp])


#%%
# calculate overall average accuracy and average median RT

subject_number = data [:,0]
stimuli = data [:,1]
pairing = data [:,2]
accuracy = data [:,3]
median = data [:,4]

acc_avg = np.mean(accuracy*100)
mrt_avg = np.mean(median)# 477.3ms


#%%
# calculate averages (accuracy & RT) split by stimulus using a for loop and an 
# if statement. (i.e., loop through the data to make a sum for each condition, 
# then divide by the number of data points going into the sum)
#
sum1=0
sum2=0
sum3=0
sum4=0

words=0
faces=0

for i in range (len(subject_number)):
    if stimuli [i]==1:
        words += 1
        sum1 = sum1 + accuracy[i]
        sum2 = sum2 + median[i]
    else:
        faces += 1
        sum3 = sum3 + accuracy[i]
        sum4 = sum4 + median[i]
        
wordsacc_avg = (sum1 / words) *100
faceacc_avg = (sum3 / faces) *100
wordsavg_median = sum2 / words
facesavg_median = sum4 / faces

# words: 88.6%, 489.4ms   faces: 94.4%, 465.3ms


#%%
# calculate averages (accuracy & RT) split by congruency using indexing, 
# slicing, and numpy's mean function 
# wp - white/pleasant, bp - black/pleasant
# (hint: only one line of code is needed per average)

wp1 = list()
wp2 = list()
bp1 = list()
bp2 = list()

for i in range(len(subject_number)):
    if pairing[i] ==1:
        wp1.append(accuracy[i])
        wp2.append(median[i])
    else:
        bp1.append(accuracy[i])
        bp2.append(median[i])
        
acc_wp =np.mean(wp1)*100
acc_bp = np.mean(bp1)*100
mrt_wp =np.mean(wp2)
mrt_bp = np.mean(bp2)


#%% 
# calculate average median RT for each of the four conditions
# use for loops, indexing/slicing, or both!
# (hint: might be easier to slice data into separate words and faces datasets)
#
wordswp = list()
wordsbp = list()
faceswp = list()
facesbp = list()

for i in range(len(subject_number)):
    if pairing[i] == 1 and stimuli[i] ==1:
        wordswp.append(median[i])
        
    elif pairing[i] == 2 and stimuli[i] == 1:
        wordsbp.append(median[i])
        
    elif pairing[i] ==1 and stimuli[i] ==2:
        faceswp.append(median[i])
        
    elif pairing[i] ==2 and stimuli[i] ==2:
        facesbp.append(median[i])
        
mrt_wordswp = np.mean(wordswp)
mrt_wordsbp = np.mean(wordsbp)

mrt_faceswp = np.mean(faceswp)
mrt_facesbp = np.mean(facesbp)



# words - white/pleasant: 478.4ms
# words - black/pleasant: 500.3ms
# faces - white/pleasant: 460.8ms
# faces - black/pleasant: 469.9ms


#%%        
# compare pairing conditions' effect on RT within stimulus using scipy's 
# paired-sample t-test: scipy.stats.ttest_rel()

import scipy.stats
#need to switch to array 
wordswp_array = np.asarray(wordswp)
wordsbp_array = np.asarray(wordsbp)

faceswp_array = np.asarray(faceswp)
facesbp_array = np.asarray(facesbp)

t1 = scipy.stats.ttest_rel(wordswp_array,wordsbp_array)
t2 = scipy.stats.ttest_rel(wordswp_array,wordsbp_array)

# words: t=-5.36, p=2.19e-5
# faces: t=-2.84, p=0.0096


#%%
# print out averages and t-test results
# (hint: use the ''.format() method to create formatted strings
#
print('\nOVERALL: {:.1f}%, {:.1f} ms'.format(acc_avg,mrt_avg))
print('\nAvg_Stimulus: {:.1f}%, {:.1f}%, {:.1f} ms,{:.1f} ms'.format(wordsacc_avg,faceacc_avg,wordsavg_median,facesavg_median))
print('\nAvg_Pairing: {:.1f}%, {:.1f}%, {:.1f} ms,{:.1f} ms'.format(acc_wp,acc_bp,mrt_wp,mrt_bp))
print('\nAvg_MedianRT: {:.1f}%, {:.1f}%, {:.1f} ms,{:.1f} ms'.format(mrt_wordswp,mrt_wordsbp,mrt_faceswp,mrt_facesbp))

print("t-test [wordswp_array,wordsbp_array]",t1)
print("t-test [faceswp_array,facesbp_array]",t2)

