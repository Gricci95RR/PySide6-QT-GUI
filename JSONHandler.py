import json
from datetime import datetime
import pandas as pd

class JSONHandler:
    def __init__(self):
        self.controller_state_list      = []
        self.yaw_angle_list             = []
        self.warning_level_list         = [0]
        self.yaw_std_list               = []
        self.error_axis1_list           = []
        self.error_axis2_list           = []
        self.yaw_offset_list            = []
        self.aar_offset_list            = []
        self.control_instability_protection_list = []
        self.min_voltage_list           = []
        self.max_voltage_list           = []
        self.open_loop_max_speed_list   = []
        self.closed_loop_max_speed_list = []
        self.min_PID_limit_list         = []
        self.max_PID_limit_list         = []
        self.prefilter_numerator_arg1   = []
        self.prefilter_numerator_arg2   = []
        self.prefilter_numerator_arg3   = []
        self.prefilter_numerator_arg4   = []
        self.prefilter_denominator_arg1 = []
        self.prefilter_denominator_arg2 = []
        self.filter_1_numerator_arg1    = []
        self.filter_1_numerator_arg2    = []
        self.filter_1_numerator_arg3    = []
        self.filter_1_numerator_arg4    = []
        self.filter_1_denominator_arg1  = []
        self.filter_1_denominator_arg2  = []
        self.filter_2_numerator_arg1    = []
        self.filter_2_numerator_arg2    = []
        self.filter_2_denominator_arg1  = []
        self.filter_3_numerator_arg1    = []
        self.filter_3_numerator_arg2    = []
        self.filter_3_denominator_arg1  = []
        self.hysteresis_compensation_list    = []
        self.compensation_offset_list        = []
        self.quadratic_parameters_arg1_list  = []
        self.quadratic_parameters_arg2_list  = []
        self.f_parameters_arg1_list     = []
        self.f_parameters_arg2_list     = []
        self.k_parameters_arg1_list     = []
        self.k_parameters_arg2_list     = []
        self.time_list                  = []
        self.counter = 0
        # --- tab 1 --- #
        controls_dict = {
            "StartM": 0,
            "StopM": 0,
            "SP (V/urad)": 0,
            "Mode": 'Absolute',
            "Re contr prot": 0,
            "Re intf prot": 0,
            "Mode": 0
        }
        self.json_to_send_controls = {
            "Controls": controls_dict
        }
        # --- tab 2 --- #
        general_settings_dict = {
            "Write general settings": 0,
            "yawOffset": 0,
            "AAROffset": 0,
            "controlInstabilityProtection": 0,
            "minVoltage": 0,
            "maxVoltage": 0,
            "openLoopMaxSpeed": 0,
            "closedLoopMaxSpeed": 0,
            "minPIDLimit": 0,
            "maxPIDLimit": 0
        }
        self.json_to_send_general_settings = {
            "General settings": general_settings_dict
        }
        
        # --- tab 3 --- #
        control_settings_dict = {
            "Write control settings": 0,
            "prefilterNumerator": [0, 0, 0, 0],
            "prefilterDenominator": [0, 0],
            "filter1Numerator": [0, 0, 0, 0],
            "filter1Denominator": [0, 0],
            "filter2Numerator": [0, 0],
            "filter2Denominator": 0,
            "filter3Numerator": [0, 0],
            "filter3Denominator": 0,
            "hysteresisCompensation": 0,
            "compensationOffset": 0,
            "quadraticParameters": [0, 0],
            "fParameters": [0, 0],
            "kParameters": [0, 0]
        }
        self.json_to_send_control_settings = {
            "Control settings": control_settings_dict
        }
        # --- tab 4 --- #
        expert_precedures_dict = {
            "Profile motion Start": 0,
            "Profile motion Stop": 0,
            "waveformID": 0,
            "Ramp cycles motion Start": 0,
            "Ramp cycles motion Stop": 0,
            "numberCycles": 0,
            "rampRate": 0,
            "Logging": 0
        }
        self.json_to_send_expert_precedures = {
            "Expert procedures": expert_precedures_dict
        }

    def parse_json_string(self, json_string):
        """
        Parse JSON data from a string.

        Parameters:
            json_string (str): The JSON string to parse.

        Returns:
            dict: A dictionary representing the parsed JSON data.
        """
        try:
            json_string = json_string.replace("'", '"')
            parsed_data = json.loads(json_string)
            first_key = list(parsed_data.keys())[0]
            # --- tab 1 --- #
            if first_key == "Controls":
                self.controller_state_list.append(parsed_data[first_key]["state"])
                self.yaw_angle_list.append(parsed_data[first_key]["yawAngle"])
                self.warning_level_list.append(parsed_data[first_key]["warninglevel"])
                self.yaw_std_list.append(parsed_data[first_key]["yawAngleStdDeviation"])
                self.error_axis1_list.append(parsed_data[first_key]["errorAxis1"])
                self.error_axis2_list.append(parsed_data[first_key]["errorAxis2"])
            # --- tab 2 --- #
            if first_key == "General settings":
                self.yaw_offset_list.append(parsed_data[first_key]["yawOffset"])
                self.aar_offset_list.append(parsed_data[first_key]["AAROffset"])
                self.control_instability_protection_list.append(parsed_data[first_key]["controlInstabilityProtection"])
                self.min_voltage_list.append(parsed_data[first_key]["minVoltage"])
                self.max_voltage_list.append(parsed_data[first_key]["maxVoltage"])
                self.open_loop_max_speed_list.append(parsed_data[first_key]["openLoopMaxSpeed"])
                self.closed_loop_max_speed_list.append(parsed_data[first_key]["closedLoopMaxSpeed"])
                self.min_PID_limit_list.append(parsed_data[first_key]["minPIDLimit"])
                self.max_PID_limit_list.append(parsed_data[first_key]["maxPIDLimit"])
            # --- tab 3 --- #
            if first_key == "Control settings":
                self.prefilter_numerator_arg1.append(parsed_data[first_key]["prefilterNumerator"][0])
                self.prefilter_numerator_arg2.append(parsed_data[first_key]["prefilterNumerator"][1])
                self.prefilter_numerator_arg3.append(parsed_data[first_key]["prefilterNumerator"][2])
                self.prefilter_numerator_arg4.append(parsed_data[first_key]["prefilterNumerator"][3])
                self.prefilter_denominator_arg1.append(parsed_data[first_key]["prefilterDenominator"][0])
                self.prefilter_denominator_arg2.append(parsed_data[first_key]["prefilterDenominator"][1])
                # filter 1
                self.filter_1_numerator_arg1.append(parsed_data[first_key]["filter1Numerator"][0])
                self.filter_1_numerator_arg2.append(parsed_data[first_key]["filter1Numerator"][1])
                self.filter_1_numerator_arg3.append(parsed_data[first_key]["filter1Numerator"][2])
                self.filter_1_numerator_arg4.append(parsed_data[first_key]["filter1Numerator"][3])
                self.filter_1_denominator_arg1.append(parsed_data[first_key]["filter1Denominator"][0])
                self.filter_1_denominator_arg2.append(parsed_data[first_key]["filter1Denominator"][1])
                # filter 2
                self.filter_2_numerator_arg1.append(parsed_data[first_key]["filter2Numerator"][0])
                self.filter_2_numerator_arg2.append(parsed_data[first_key]["filter2Numerator"][1])
                self.filter_2_denominator_arg1.append(parsed_data[first_key]["filter2Denominator"])
                # filter 3
                self.filter_3_numerator_arg1.append(parsed_data[first_key]["filter3Numerator"][0])
                self.filter_3_numerator_arg2.append(parsed_data[first_key]["filter3Numerator"][1])
                self.filter_3_denominator_arg1.append(parsed_data[first_key]["filter3Denominator"])

                self.hysteresis_compensation_list.append(parsed_data[first_key]["hysteresisCompensation"])
                self.compensation_offset_list.append(parsed_data[first_key]["compensationOffset"])
                
                self.quadratic_parameters_arg1_list.append(parsed_data[first_key]["quadraticParameters"][0])
                self.quadratic_parameters_arg2_list.append(parsed_data[first_key]["quadraticParameters"][1])
                
                self.f_parameters_arg1_list.append(parsed_data[first_key]["fParameters"][0])
                self.f_parameters_arg2_list.append(parsed_data[first_key]["fParameters"][1])
                self.k_parameters_arg1_list.append(parsed_data[first_key]["kParameters"][0])
                self.k_parameters_arg2_list.append(parsed_data[first_key]["kParameters"][1])
            if first_key == "Logging":
                current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                filename_Axis1Logging = f"logging\\Logging_{current_datetime}.csv"
                even_items = parsed_data["Logging"][::2]
                odd_items = parsed_data["Logging"][1::2]
                df = pd.DataFrame({'Yaw angle (urad)': even_items, 'Output voltage (V)': odd_items})
                df.to_csv(filename_Axis1Logging, index=False)
            self.counter = self.counter + 1
            self.time_list.append(self.counter)
            return parsed_data
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None