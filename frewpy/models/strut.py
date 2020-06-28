from typing import List, Union

from .exceptions import FrewError


class StrutObj():
    def __init__(
        self,
        id: int,
        flags: int = 0,
        stage_in: int = -1,
        stage_out: int = -1,
        node_strut: int = 1,
        prestress: float = 0,
        stiffness: float = 1000000000,
        angle: float = 0,
        lever_arm: float = 0,
        level_strut: float = 0,
        horz_force: float = 0,
        is_iba_generated: bool = False,
        is_seismic: bool = False
    ):
        self.id = id
        self.flags = flags
        self.stage_in = stage_in
        self.stage_out = stage_out
        self.node_strut = node_strut
        self.prestress = prestress
        self.stiffness = stiffness
        self.angle = angle
        self.lever_arm = lever_arm
        self.level_strut = level_strut
        self.horz_force = horz_force
        self.is_iba_generated = is_iba_generated
        self.is_seismic = is_seismic


class Strut:
    def __init__(self, json_data: dict):
        self.json_data = json_data
        self._check_json_data()
        self.strut_dicts = self.json_data["Struts"]

    def _check_json_data(self) -> None:
        if not self.json_data.get("Struts", False):
            raise FrewError("No struts defined in the model")

    @staticmethod
    def _check_node_input_type(node: int) -> None:
        if type(node) != int:
            raise FrewError("Input node must be an integer.")

    def get_struts(self) -> List[StrutObj]:
        """ Get a list of all the strut objects within the Frew model.

        Returns
        -------
        struts : List[StrutObj]
            A list of struts in the Frew model.

        """
        self._check_json_data()
        struts = []
        for i, strut_dict in enumerate(self.strut_dicts, 1):
            args = list(strut_dict.values())
            args.insert(0, i)
            struts.append(StrutObj(*args))
        return struts

    def get_strut_by_node(
        self, node: int
    ) -> StrutObj:
        """ Get a strut object at the specified node location within the Frew
        model. If more than one strut is found, the first strut occurence is
        returned.

        Parameters
        ----------
        node : int
            The node number of the strut

        Returns
        -------
        strut : StrutObj
            A strut object in the Frew model matching the input node number.

        """
        self._check_node_input_type(node)
        self._check_json_data()

        for strut in self.get_struts():
            if strut.node_strut == node:
                return strut

        raise FrewError(
            f"There is no strut defined at node {node} in the model"
        )

    def get_struts_by_node(self, node: int) -> List[StrutObj]:
        """ Get a list of strut objects at the specified node location within
        the Frew model.

        Parameters
        ----------
        node : int
            The node number of the strut

        Returns
        -------
        struts : List[StrutObj]
            A list of struts in the Frew model.

        """
        self._check_node_input_type(node)
        self._check_json_data()

        struts = [
            strut for strut in self.get_struts() if strut.node_strut == node
        ]
        if struts:
            return struts
        else:
            raise FrewError(
                f"There are no struts defined at node {node} in the model"
            )

    def _set_strut_vals(self, strut: StrutObj, strut_dict: dict) -> None:
        # Get list of strut object values excluding the ID
        new_vals = list(strut.__dict__.values())[1:]

        for key, val in zip(strut_dict.keys(), new_vals):
            strut_dict[key] = val

    def set(self, struts: Union[StrutObj, List[StrutObj]]) -> None:
        if type(struts) == list:
            for strut, strut_dict in zip(struts, self.strut_dicts):
                self._set_strut_vals(strut, strut_dict)

        if type(struts) == StrutObj:
            strut_dict = self.strut_dicts[struts.id - 1]
            self._set_strut_vals(struts, strut_dict)

    # def remove(self, struts: Union[StrutObj, List[StrutObj]]):
    #     if type(struts) == list:
    #         for strut in struts:
    #             self.strut_dicts.remove(self.strut_dicts[struts.id - 1])

    #     if type(struts) == StrutObj:
    #         self.strut_dicts.remove(self.strut_dicts[struts.id - 1])

    def add(self, struts: Union[StrutObj, List[StrutObj]]):
        pass
