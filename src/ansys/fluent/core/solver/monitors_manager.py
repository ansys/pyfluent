"""Module for events management."""
import itertools
import threading
from functools import partial
from typing import Callable, List
import pandas as pd 
from ansys.api.fluent.v0 import monitor_pb2 as MonitorModule
pd.options.plotting.backend = "plotly"

class MonitorsManager:
    """
    Manages the server side events.
    Allows client to register/unregister callbacks with server events.

    Parameters
    ----------
    session_id : str
        Session id.
    service :
        Event streaming service.

    Properties
    ----------
    events_list : List[str]
        List of supported events.
    """

    def __init__(self, session_id: str, service):
        self._session_id: str = session_id
        self._monitors_service = service              
        self._lock: threading.Lock = threading.Lock()        
        self._monitors_info = None
        self._monitors_thread = None 
        self._data_frames ={}
        
    def get_monitor_sets_name(self):
         with self._lock:
             return list(self._data_frames.keys())
             
    def get_monitor_set_prop(self, monitor_set_name, prop):
         with self._lock:             
             return self._monitors_info.get(monitor_set_name,{}).get(prop)           
             
    def get_monitor_set_data(self, monitor_set_name):
         with self._lock: 
            df = self._data_frames[monitor_set_name]["df"]         
            return None if df.empty else df.plot()            

    def get_monitors_info(self):
        return self._monitors_service.get_monitors_info()    
    
    def _begin_streaming(self):
        responses = self._monitors_service.begin_streaming()        
        while True:            
            try:    

                data_raceived = {}            
                response = next(responses)
                x_axis_type = response.xaxisdata.xaxistype
                x_axis_index = response.xaxisdata.xaxisindex
                data_raceived["xvalues"]=x_axis_index                
                for y_axis_value in response.yaxisvalues:                   
                    data_raceived[y_axis_value.name]=y_axis_value.value
                    
                with self._lock:
                    for monitor_set_name, df_data in self._data_frames.items():
                        df = df_data["df"]
                        monitors = df_data["monitors"]
                        monitor_data =[]
                        for monitor_name in monitors:
                            if monitor_name not in data_raceived:
                                monitor_data =[]
                                break                                 
                            monitor_data.append(data_raceived[monitor_name]) 
                        
                        if monitor_data:                        
                            new_df = pd.DataFrame([monitor_data], columns=monitors)
                            new_df.set_index('xvalues', inplace=True)
                            df_data["df"] = df.append(new_df)
                        
                       
            except StopIteration:
                print('StopIteration')
                break
      
   
    def refresh(self, session_id, event_info):
        print('monitor manager refresh')
        if self._monitors_thread: 
            self.stop() 
            self.start() 
    
    def start(
        self
    ) -> str:
        """
        Register Callback.

        Parameters
        ----------
        event_name : str
            Event name to which callback should be registered.

        call_back : Callable
            Callback to register.

        Raises
        ------
        RuntimeError
            If event name is not valid.

        Returns
        -------
        str
            Registered callback Id.

        """    
        if not self._monitors_thread:                  
            self._monitors_info = self.get_monitors_info()
            print('reset dataframe')
            self._data_frames ={}
            for monitor_set_name, monitor_set_info in self._monitors_info.items():
                self._data_frames[monitor_set_name] = {}
                monitors_name = list(monitor_set_info['monitors'])+["xvalues"]
                df = pd.DataFrame([], columns=monitors_name)
                df.set_index('xvalues', inplace=True)
                self._data_frames[monitor_set_name]["df"]= df
                  
                self._data_frames[monitor_set_name]["monitors"]= monitors_name
                
              
                
            self._monitors_thread: threading.Thread = threading.Thread(
                target=MonitorsManager._begin_streaming, args=(self,)
            )        
                    
            self._monitors_thread.start()
           
                 

   

    def stop(self):
        """
        Stop Events manager.
        """
        with self._lock:
            if self._monitors_thread:
                print('monitor manager', 'stop')
                self._monitors_service.end_streaming()
                self._monitors_thread.join()
                self._monitors_thread = None 
