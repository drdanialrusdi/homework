# -*- coding: utf-8 -*-
"""
Created on Fri Jun  1 14:37:42 2018

@author: 00130161
"""

import numpy as np

def randomduration(durationlist, num_call=1):
    '''
    return random duration of incoming call 
    '''
    return np.random.choice(durationlist,num_call)



def incomingcall(incominglist,random=True,num_call=1):
    '''
    return the time slot where incoming call would happen in range 0 to 3600
    '''
    if random:
        return sorted(np.random.choice(incominglist,num_call))
    else:
        return sorted(incominglist)

def abandon_call(abandonlist,num_call=1):
    '''
    '''
    return np.random.choice(abandonlist,num_call)


def simulation_model(incominglist, durationlist, num_call, abandonlist, max_agent=24, numcall_follow_poisson=False):
    
    #If true, numcall will based on poisson instead of prediction
    if numcall_follow_poisson:
        num_call=np.random.poisson(num_call,1)
    
    #offeredcallinonehour. Must be constant for every agent testing
    offered_call=incomingcall(incominglist,num_call=num_call)
    
    
    #Simulate for all the number of agent
    abandon_per_agent={}
    final_waitinglist_per_agent={}
    
    
    for agent in range(max_agent):
        #time agent start conversation. If no conversation, it reset to 0
        agent_work=np.zeros(agent+1)
        #time agent finish conversation
        agent_time=np.zeros(agent+1)
        #Initiate waitinglist and time to abandon list variable
        waitinglist=[]
        time_to_abandon=[]
        abdn_cust=[]
        #print("Agent :",agent+1)
        #time arrival for incoming call
        for call in offered_call:
            #print("The Call:",call)
            #update the status of agent work. Assign the waitinglist to free agent
            #Sort the agent based on who finish first
            sort_index_agent_time=np.argsort(agent_time)
            agent_time=agent_time[sort_index_agent_time]
            agent_work=agent_work[sort_index_agent_time]
            for index,finishtime in enumerate(agent_time):
                #if agent already finish the conversation at the arrival the call. Reset to 0
                
                if finishtime < call:
                    agent_work[index]=0
                    agent_time[index]=0
                    #Assign the waiting list to this call.Below function mean customer not abandon yet
                    #Test whether there are people in waiting list or not
                    try:
                        #See if customer not abandon yet and assign it to the free staf
                        if time_to_abandon[0]>finishtime:
                            waitinglist.pop(0)
                            time_to_abandon.pop(0)
                            agent_work[index]=finishtime
                            agent_time[index]=finishtime+randomduration(durationlist)+np.round(np.random.uniform(15,45,1))
                    except IndexError:
                        continue
                    
                    
            #update time to abandon and waiting list
            if bool(time_to_abandon):
                for cust in time_to_abandon:
                    if cust<call:
                        #Store the abandon customer and remove the abandon customer from waitinglist.Always the first waiting list abandon
                        abdn_cust.append(waitinglist.pop(0))
                        time_to_abandon.pop(0)
                        #print("len abndon customer",abdn_cust)
            
            
            #checking if there are free agent
            if np.min(agent_work)==0:
                #if no one in waiting list. Assign to agent
                if len(waitinglist)==0:
                    #assign the free agent with incoming call
                    free_agent=np.argmin(agent_work)
                    agent_work[free_agent]=call
                    #assign the time agent finish the conversation
                    agent_time[free_agent]=call+randomduration(durationlist)+np.round(np.random.uniform(15,45,1))
                    #print("agent_time",agent_time)
            #if no free agent. Assign to the waitinglist
            else:
                #time when customer start onhold
                waitinglist.append(call)
                #time when customer abandon the call. It should have same length 
                time_to_abandon.append(call+abandon_call(abandonlist))
                
            
        #update abandon customer after 1 hour
        if bool(time_to_abandon):
            for cust in time_to_abandon:
                #for 1 hour
                if cust<3600:
                    #Store the abandon customer and remove the abandon customer from waitinglist.Always the first waiting list abandon
                    abdn_cust.append(waitinglist.pop(0))
                    time_to_abandon.pop(0)
            
            
        abandon_per_agent[agent+1]=abdn_cust
        final_waitinglist_per_agent[agent+1]=waitinglist
        
    return abandon_per_agent,final_waitinglist_per_agent,offered_call

def number_of_simulation(n_simulation,incominglist, durationlist, num_call, abandonlist, max_agent=24,  numcall_follow_poisson=False):
    Agents=np.zeros(max_agent)

    #Repeat the simulation model based on n_simulation
    for simulation in range(n_simulation):
        abandon_per_agent,final_waitinglist_per_agent,offered_call=simulation_model(incominglist, durationlist, num_call, abandonlist, max_agent, numcall_follow_poisson=False)
        #For each agent dictionary 1 to max
        for agent in abandon_per_agent.keys():
            Agents[agent-1]=Agents[agent-1]+len(abandon_per_agent[agent])
    avg_abandon_per_agent=Agents/n_simulation
    avg_abandon_percentage_per_agent=(Agents/num_call)/n_simulation
        
    return avg_abandon_per_agent, avg_abandon_percentage_per_agent