# AUTOGENERATED! DO NOT EDIT! File to edit: 01_discovery.ipynb (unless otherwise specified).

__all__ = ['DataFlows', 'DataStructure']

# Cell
from .base import ISTAT
from .utils import make_tree, strip_ns
import pandas as pd

# Cell
class DataFlows(ISTAT):
    """Base class to explore available Dataflows"""
    def __init__(self):
        super().__init__()
        self.resource = "dataflow"
        self.available = self.all_available()

    def parse_dataflows(self, response):
        """parse the `response` containing all the available datasets and return a list of dataflows."""
        tree = make_tree(response)
        strip_ns(tree)
        root = tree.root

        dataflows_l = []
        for dataflow in root.iter('Dataflow'):
            id = dataflow.get('id')
            version = dataflow.get('version')
            structure_id = [ref.get('id') for ref in dataflow.iter('Ref')][0]

            #iter over names and get the descriptions
            for name in dataflow.findall('Name'):
                lang = name.get("{http://www.w3.org/XML/1998/namespace}lang")
                if lang == 'en':
                    description_en = name.text
                #if lang == 'it':
                    #description_it = name.text

            dataflow_dict = {
            "df_id": id,
            "version": version,
            "description": description_en,
            #"description_it": description_it,
            "df_structure_id": structure_id,
            }

            dataflows_l.append(dataflow_dict)

        return dataflows_l

    def all_available(self, dataframe = True):
        """Return all available dataflows"""
        path = 'dataflow/IT1'
        response = self._request(path = path)
        dataflows = self.parse_dataflows(response)

        if dataframe == True: dataflows = pd.DataFrame(dataflows)

        return dataflows

    def search(self, keyword):
        """Search available dataflows that contain `keyword`. Return these dataflows in a DataFrame"""
        dataflows = self.available[self.available['description'].str.contains(keyword, case=False)]

        return dataflows

# Cell
class DataStructure(ISTAT):
        """Class that implements methods to retrieve informations about a Dataset"""
        def __init__(self):
            super().__init__()
            self.resource = "datastructure"
            self.available = DataFlows().available #df with all the available dataflows
            #TODO: Initiate the class with a specific dataset. Retrieve informations only on it (maybe use a dataset loader)

        def get_df_structure_id(self, **kwargs):
            """Return the `df_structure_id` of a dataflow from its `df_id` or `df_description`"""
            valid_args = ['df_description', 'df_id']

            arg = [*kwargs][0]
            arg_value = [x for x in kwargs.values()][0]

            #arguments errors
            if arg not in valid_args: raise ValueError(f"{arg} is not a valid argument. Use one of: {', '.join(valid_args)}")
            #elif lang not in ['en', 'it']: raise ValueError("'lang' must be 'en' (English) or 'it' (Italian)")

            if arg == "df_description": mask = self.available["description"] == arg_value
            else: mask = self.available[arg] == arg_value

            df_structure_id = self.available[mask].df_structure_id.values[0]
            return df_structure_id

        def get_df_id(self, **kwargs):
            """Return the `df_id` of a dataflow from its `df_description` or `df_structure_id`"""
            valid_args = ['df_description', 'df_structure_id']

            arg = [*kwargs][0]
            arg_value = [x for x in kwargs.values()][0]

            #arguments errors
            if arg not in valid_args: raise ValueError(f"{arg} is not a valid argument. Use one of: {', '.join(valid_args)}")
            #elif lang not in ['en', 'it']: raise ValueError("'lang' must be 'en' (English) or 'it' (Italian)")

            if arg == "df_description" : mask = self.available["description"] == arg_value
            else : mask = self.available[arg] == arg_value

            df_id = self.available[mask].df_id.values[0]
            return df_id

        def get_df_description(self, lang = 'en', **kwargs):
            """Return the `df_description` of a dataflow from its `df_id` or `df_structure_id`"""
            valid_args = ['df_id', 'df_structure_id']

            arg = [*kwargs][0]
            arg_value = [x for x in kwargs.values()][0]

            #arguments errors
            if arg not in valid_args: raise ValueError(f"{arg} is not a valid argument. Use one of: {', '.join(valid_args)}")
            #elif lang not in ['en', 'it']: raise ValueError("'lang' must be 'en' (English) or 'it' (Italian)")

            mask = self.available[arg] == arg_value
            df_description = self.available[mask].description.values[0]
            return df_description

        def parse_dimensions(self, response):
            """Parse the `response` containing a dataflow's dimensions and return them in a list"""
            tree = make_tree(response)
            strip_ns(tree)
            root = tree.root
            print(root)

            dimensions_l = []
            for dimension in root.iter('Dimension'):
                dimension_name = dimension.attrib['id']

                dimension_id = [enumeration.find('Ref').get('id') for enumeration in dimension.iter('Enumeration')][0]

                dimension_dict = {'dimension' : dimension_name,
                                  'dimension_ID' : dimension_id}

                dimensions_l.append(dimension_dict)

            return(dimensions_l)

        def dimensions_description(self, dimensions):
            """Return a dataframe with the descriptions of `dimensions`"""
            resource = "codelist"
            dimensions_l = dimensions.dimension_ID.tolist()
            descriptions_l = []

            for dimension_id in dimensions_l:
                path_parts = [resource, self.agencyID, dimension_id]
                path = "/".join(path_parts)
                response = self._request(path = path)
                tree = make_tree(response)
                strip_ns(tree)
                root = tree.root

                description = [x for x in root.iter('Codelist')][0]
                #description_it = description.findall('Name')[0].text
                description = description.findall('Name')[1].text

                description_dict = {'dimension_ID' : dimension_id,
                                   'description' : description}
                descriptions_l.append(description_dict)

            dimensions_descriptions = pd.DataFrame(descriptions_l)

            return dimensions_descriptions

        def get_dimensions(self, dataframe = True, **kwargs):
            """Return a Dataframe containing the dimensions (and their descriptions) of a specific dataflow."""
            valid_args = ['df_id', 'df_structure_id', 'df_description']

            arg = [*kwargs][0]
            arg_value = [x for x in kwargs.values()][0]

            #arguments errors
            if arg not in valid_args: raise ValueError(f"{arg} is not a valid argument. Use one of: {', '.join(valid_args)}")

            if arg != 'df_structure_id': df_structure_id = self.get_df_structure_id(**{arg : arg_value})
            else: df_structure_id = arg_value

            path_parts = [self.resource, self.agencyID, df_structure_id]
            path = "/".join(path_parts)
            response = self._request(path = path)
            dimensions = self.parse_dimensions(response)

            if dataframe == True: dimensions = pd.DataFrame(dimensions)
            dimensions_description = self.dimensions_description(dimensions)
            dimensions = dimensions.merge(dimensions_description, on='dimension_ID')

            return dimensions

        def get_dimension_values(self, dimension_ID, dataframe = True):
            """Return the possible values of a dimension"""
            resource = "codelist"
            path_parts = [resource, self.agencyID, dimension_ID]
            path = "/".join(path_parts)
            response = self._request(path = path)
            tree = make_tree(response)
            strip_ns(tree)
            root = tree.root

            values = []
            for value in root.iter('Code'):
                value_id = value.get('id')
                #value_it = value.findall('Name')[0].text
                value = value.findall('Name')[1].text

                value_dict = {'value_ID' : value_id,
                           'description' : value}

                values.append(value_dict)

            if dataframe == True : values = pd.DataFrame(values)
            return values
