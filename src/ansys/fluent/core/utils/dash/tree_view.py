import yaml
class TreeView:

    _tree_views = {}

    def __init__(
        self, app, connection_id, session_id, SessionsManager
    ):
        unique_id = f"tree-{connection_id}-{session_id}"
        tree_state = TreeView._tree_views.get(unique_id)
        if not tree_state:
            TreeView._tree_views[unique_id] = self.__dict__
            self._state = {}
            self.SessionsManager = SessionsManager
            self._connection_id = connection_id
            self._unique_id = unique_id
            self.session_id = session_id
            self._app = app
        else:
            self.__dict__ = tree_state
            
    def populate_tree(self, data):
        children = []
        for item_name, item_data in data.items():
            tree_data = {}
            tree_data["title"] = item_name
            remote = item_data.get("remote")
            local = item_data.get("local")
            if local:
                tree_data["key"] = f"local:{local}"
            elif remote:
                tree_data["key"] = f"remote:{remote}"
            else:
                tree_data["key"] = ""
            
            if item_data.get("children"):
                tree_data["children"] = self.populate_tree(item_data["children"])
            elif remote:
                static_info = self.SessionsManager(self._app, self._connection_id, self.session_id).static_info
                obj = self.SessionsManager(self._app, self._connection_id, self.session_id).settings_root
                path_list = remote.split("/")
                
                for path in path_list:
                    try:
                        obj = getattr(obj, path)
                        static_info = static_info["children"][obj.scheme_name]                    
                    except AttributeError:
                        obj = obj[path] 
                        static_info =  static_info['object-type'] 
                if static_info['type']=='named-object':
                    if not obj.is_active():  
                        continue
                    children_name =  list(obj.get_state().keys()) 
                    if children_name:                    
                        tree_data["key"] =""                    
                        children_data = {child:{'remote':f"{remote}/{child}"}  for child in children_name}
                        tree_data["children"] = self.populate_tree(children_data)
            children.append(tree_data)                        
                                     
        return children



    def get_tree_nodes(self, yaml_file="E:\\ajain\\ANSYSDev\\vNNN\\pyfluent\\src\\ansys\\fluent\\core\\utils\\dash\\outline.yaml"):

        with open(yaml_file           
        ) as f:
            data = yaml.load(f, Loader=yaml.SafeLoader)
        print(data)    
        print(self.populate_tree(data)[0])    
        return self.populate_tree(data)[0]  
