from PySide6.QtWidgets import (
    QApplication, QWidget,
    QVBoxLayout, QTabWidget,
    QLabel, QLineEdit,
    QGridLayout, QCheckBox,
    QPushButton, QSpinBox,
    QDoubleSpinBox, QComboBox,
    QFrame, QMessageBox
    )
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon, QFont
from datetime import datetime
from Serial import SerialThread
from JSONHandler import JSONHandler
import json

class Widget(QWidget):
    def __init__(self):
        """
        Initializes the widget.

        This method sets up the window title, geometry, layout, tab widget, and adds tabs to the widget.

        Args:
            None

        Returns:
            None
        """
        super().__init__()
        self.setWindowTitle("Sapphire Testbench")
        self.setWindowIcon(QIcon('C:\\Users\\giricci\\Desktop\\sapphire\\gui\\logo.PNG'))
        self.setGeometry(200, 200, 600, 400)
        
        font = QFont("Calibri", 12)
        QApplication.setFont(font)

        self.layout = QVBoxLayout(self)
        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)
        
        self.setup_tabs()
        
        self.jsonHandlerObj = JSONHandler()

        self.create_tab_controls_ui()
        self.create_tab_general_settings_ui()
        self.create_tab3_control_settings_ui()
        self.create_tab4_expert_procedures_ui()

        self.serial_thread = SerialThread()
        self.serial_thread.data_received.connect(self.handle_serial_data)

    def setup_tabs(self):
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()

        self.tab_widget.addTab(self.tab1, "Controls")
        self.tab_widget.addTab(self.tab2, "General settings")
        self.tab_widget.addTab(self.tab3, "Control settings")
        self.tab_widget.addTab(self.tab4, "Expert procedures")

    # -- Methods tab 1 -- #
    def create_tab_controls_ui(self):
        """
        Creates UI elements for the 'Controls' tab.

        Args:
            None

        Returns:
            None
        """
        layout = QGridLayout(self.tab1)
        # Control Mode
        self.create_control_mode_section(layout)
        # Motion control
        self.create_motion_control_section(layout)
        # Acquisition
        self.create_acquisition_section(layout)
        # Errors
        self.create_errors_section(layout, self.jsonHandlerObj.warning_level_list[-1])
        # Error reset
        self.create_error_reset_section(layout)
        # Serial Connection
        self.create_serial_connection_section(layout)

    def create_control_mode_section(self, layout):
        """
        Creates Control Mode section.

        Args:
            layout: Layout for the Controls tab.

        Returns:
            None
        """
        layout.addWidget(QLabel("<b>Control mode</b>"), 0, 0)
        layout.addWidget(QLabel("Mode"), 1, 0)
        self.combo_box_mode = QComboBox()
        self.combo_box_mode.addItems(["Standby", "Open Loop", "Closed Loop"])
        layout.addWidget(self.combo_box_mode, 1, 1)
        self.combo_box_mode.currentIndexChanged.connect(self.on_combobox_mode_changed)

    def create_motion_control_section(self, layout):
        """
        Creates Motion Control section.

        Args:
            layout: Layout for the Controls tab.

        Returns:
            None
        """
        layout.addWidget(QLabel("<b>Motion control</b>"), 3, 0)
        self.setpoint_label = QLabel("Setpoint")
        layout.addWidget(self.setpoint_label, 4, 0)
        self.setpoint_box = QDoubleSpinBox()
        self.setpoint_box.setDecimals(6)
        self.setpoint_box.setRange(-999, 999)
        layout.addWidget(self.setpoint_box, 4, 1)

        button_start_motion = QPushButton("Start Motion")
        button_start_motion.clicked.connect(self.start_motion)
        layout.addWidget(button_start_motion, 4, 2)
        button_stop_motion = QPushButton("Stop Motion")
        button_stop_motion.clicked.connect(self.stop_motion)
        layout.addWidget(button_stop_motion, 4, 3)

        self.combo_box_motion_mode = QComboBox()
        layout.addWidget(QLabel("Motion Mode"), 5, 0)
        self.combo_box_motion_mode.addItems(["Absolute", "Relative"])
        layout.addWidget(self.combo_box_motion_mode, 5, 1)

    def create_acquisition_section(self, layout):
        """
        Creates Acquisition section.

        Args:
            layout: Layout for the Controls tab.

        Returns:
            None
        """
        layout.addWidget(QLabel("<b>Acquisition</b>"), 7, 0)
        layout.addWidget(QLabel("Controller state"), 8, 0)
        layout.addWidget(QLabel("Yaw angle (urad)"), 9, 0)
        layout.addWidget(QLabel("Yaw std (urad)"), 10, 0)

        self.info_controller_state = QLineEdit()
        self.info_controller_state.setReadOnly(True)
        layout.addWidget(self.info_controller_state, 8, 1)
        self.info_yaw_angle = QLineEdit()
        self.info_yaw_angle.setReadOnly(True)
        layout.addWidget(self.info_yaw_angle, 9, 1)
        self.info_yaw_std = QLineEdit()
        self.info_yaw_std.setReadOnly(True)
        layout.addWidget(self.info_yaw_std, 10, 1)

    def create_errors_section(self, layout, warning_level):
        """
        Creates Errors section.

        Args:
            layout: Layout for the Controls tab.

        Returns:
            None
        """
        layout.addWidget(QLabel("<b>Errors</b>"), 11, 0)
        layout.addWidget(QLabel("Head Error 1"), 12, 0)
        layout.addWidget(QLabel("Head Error 2"), 13, 0)
        layout.addWidget(QLabel("Unstable controller"), 12, 2)

        self.create_led_error_widgets(layout, warning_level)

    def create_led_error_widgets(self, layout, warning_level):
        """
        Creates LED indicators for errors.

        Args:
            layout: Layout for the Controls tab.

        Returns:
            None
        """
        self.led_head_error_1 = QFrame()
        self.led_head_error_1.setFixedSize(15, 15)
        self.led_head_error_1.setFrameShape(QFrame.StyledPanel)

        self.led_head_error_2 = QFrame()
        self.led_head_error_2.setFixedSize(15, 15)
        self.led_head_error_2.setFrameShape(QFrame.StyledPanel)

        self.led_unstable_interferometer = QFrame()
        self.led_unstable_interferometer.setFixedSize(15, 15)
        self.led_unstable_interferometer.setFrameShape(QFrame.StyledPanel)
        if (warning_level == 1):
            self.led_unstable_interferometer.setStyleSheet("background-color: red")
        else:
            self.led_unstable_interferometer.setStyleSheet("background-color: white")
            
        layout.addWidget(self.led_head_error_1, 12, 1)
        layout.addWidget(self.led_head_error_2, 13, 1)
        layout.addWidget(self.led_unstable_interferometer, 12, 3)

    def create_error_reset_section(self, layout):
        """
        Creates Error Reset section.

        Args:
            layout: Layout for the Controls tab.

        Returns:
            None
        """
        layout.addWidget(QLabel("<b>Errors</b>"), 11, 4)
        button_reset_control_protection = QPushButton("Reset control and interferometer protection")
        button_reset_control_protection.clicked.connect(self.reset_control_protection)
        layout.addWidget(button_reset_control_protection, 12, 4)
        #button_reset_interferometer_protection = QPushButton("Reset interferometer protection")
        #button_reset_interferometer_protection.clicked.connect(self.reset_interferometer_protection)
        #layout.addWidget(button_reset_interferometer_protection, 12, 5)

    def create_serial_connection_section(self, layout):
        """
        Creates Serial Connection section.

        Args:
            layout: Layout for the Controls tab.

        Returns:
            None
        """
        self.button_connect_serial = QPushButton("Connect")
        self.button_connect_serial.clicked.connect(self.connect_serial)
        layout.addWidget(self.button_connect_serial, 15, 2)

        self.button_disconnect_serial = QPushButton("Disconnect")
        self.button_disconnect_serial.clicked.connect(self.disconnect_serial)
        layout.addWidget(self.button_disconnect_serial, 15, 3)
        
        self.button_connect_serial.setEnabled(True)
        self.button_disconnect_serial.setEnabled(False)

    def start_motion(self):
        """
        Method to handle starting motion.
        """
        setpoint_value = self.setpoint_box.value()
        combo_box_value = self.combo_box_motion_mode.currentText()
        self.jsonHandlerObj.json_to_send_controls["Controls"]["StartM"] = 1
        self.jsonHandlerObj.json_to_send_controls["Controls"]["StopM"] = 0
        self.jsonHandlerObj.json_to_send_controls["Controls"]["SP (V/urad)"] = setpoint_value
        self.jsonHandlerObj.json_to_send_controls["Controls"]["Mode"] = combo_box_value
        self.serial_thread.write_to_serial(json.dumps(self.jsonHandlerObj.json_to_send_controls))
        self.jsonHandlerObj.json_to_send_controls["Controls"]["StartM"] = 0
        self.serial_thread.write_to_serial(json.dumps(self.jsonHandlerObj.json_to_send_controls))

    def stop_motion(self):
        """
        Method to handle stopping motion.
        """
        setpoint_value = self.setpoint_box.value()
        combo_box_value = self.combo_box_motion_mode.currentText()
        self.jsonHandlerObj.json_to_send_controls["Controls"]["StartM"] = 0
        self.jsonHandlerObj.json_to_send_controls["Controls"]["StopM"] = 1
        self.jsonHandlerObj.json_to_send_controls["Controls"]["SP (V/urad)"] = setpoint_value
        self.jsonHandlerObj.json_to_send_controls["Controls"]["Mode"] = combo_box_value
        self.serial_thread.write_to_serial(json.dumps(self.jsonHandlerObj.json_to_send_controls))
        self.jsonHandlerObj.json_to_send_controls["Controls"]["StopM"] = 0
        self.serial_thread.write_to_serial(json.dumps(self.jsonHandlerObj.json_to_send_controls))
    
    def reset_control_protection(self):
        """
        Method to handle reset control protection.
        """
        self.jsonHandlerObj.json_to_send_controls["Controls"]["Re contr prot"] = 1
        self.serial_thread.write_to_serial(json.dumps(self.jsonHandlerObj.json_to_send_controls))
        self.jsonHandlerObj.json_to_send_controls["Controls"]["Re contr prot"] = 0
        self.serial_thread.write_to_serial(json.dumps(self.jsonHandlerObj.json_to_send_controls))
    
    '''def reset_interferometer_protection(self):
        """
        Method to handle reset interferometer protection.
        """
        self.jsonHandlerObj.json_to_send_controls["Controls"]["Re intf prot"] = 1
        self.serial_thread.write_to_serial(json.dumps(self.jsonHandlerObj.json_to_send_controls))
        self.jsonHandlerObj.json_to_send_controls["Controls"]["Re intf prot"] = 0'''

    def set_led_head_error_1_color(self, error_signal):
        if (error_signal == "0"):
            self.led_head_error_1.setStyleSheet("background-color: " + "green")
        else:
            self.led_head_error_1.setStyleSheet("background-color: " + "red")
    
    def set_led_head_error_2_color(self, error_signal):
        if (error_signal == "0"):
            self.led_head_error_2.setStyleSheet("background-color: " + "green")
        else:
            self.led_head_error_2.setStyleSheet("background-color: " + "red")

    def on_combobox_mode_changed(self):
        """
        Method to be executed when the mode changes
        """
        selected_item = self.combo_box_mode.currentText()
        print(f"Combobox changed: {selected_item}")
        combo_box_value = self.handle_selection_mode(selected_item)
        self.jsonHandlerObj.json_to_send_controls["Controls"]["Mode"] = combo_box_value
        self.serial_thread.write_to_serial(json.dumps(self.jsonHandlerObj.json_to_send_controls))
           
    def handle_selection_mode(self, selection):
        if selection == "Standby":
            self.setpoint_label.setText("Setpoint")
            return 0
        elif selection == "Open Loop":
            self.setpoint_label.setText("Setpoint (V)")
            return 1
        elif selection == "Closed Loop":
            self.setpoint_label.setText("Setpoint (urad)")
            return 2
        else:
            print("Unknown mode selected.")

    def connect_serial(self):
        self.serial_thread.start()
        self.button_connect_serial.setEnabled(False)
        self.button_disconnect_serial.setEnabled(True)

    def disconnect_serial(self):
        self.serial_thread.stop()
        self.button_connect_serial.setEnabled(True)
        self.button_disconnect_serial.setEnabled(False)

    # -- Methods Tab 2 -- #
    def create_tab_general_settings_ui(self):
        """
        Creates UI elements for the 'General settings' tab.

        Args:
            None

        Returns:
            None
        """
        layout = QGridLayout(self.tab2)

        # -- Offsets -- #
        self.add_label(layout, "<b>Offsets</b>", 0, 0)
        label_yaw_offset = self.add_label(layout, "Yaw offset (urad)", 1, 0)
        label_aar_offset = self.add_label(layout, "AAR offset (pm)", 2, 0)

        self.info_yaw_offset = self.create_spin_box()
        self.add_widget(layout, self.info_yaw_offset, 1, 1)
        
        self.info_aar_offset = self.create_spin_box()
        self.add_widget(layout, self.info_aar_offset, 2, 1)

        # -- Protection layers -- #
        self.add_label(layout, "<b>Protection layers</b>", 3, 0)
        label_control_protection = self.add_label(layout, "Control instability protection", 4, 0)

        self.checkbox_control_instability_protection = self.create_checkbox()
        self.add_widget(layout, self.checkbox_control_instability_protection, 4, 1)

        # -- Software limits -- #
        self.add_label(layout, "<b>Software limits</b>", 6, 0)
        label_min_voltage           = self.add_label(layout, "Min voltage (V)", 7, 0)
        label_max_voltage           = self.add_label(layout, "Max voltage (V)", 8, 0)
        label_open_loop_max_speed   = self.add_label(layout, "Open loop max speed (V/s)", 9, 0)
        label_closed_loop_max_speed = self.add_label(layout, "Closed loop max speed (urad/s)", 10, 0)
        label_min_pid_limit         = self.add_label(layout, "Min PID limit", 11, 0)
        label_max_pid_limit         = self.add_label(layout, "Max PID limit", 12, 0)

        self.info_min_voltage = self.create_spin_box()
        self.add_widget(layout, self.info_min_voltage, 7, 1)

        self.info_max_voltage = self.create_spin_box()
        self.add_widget(layout, self.info_max_voltage, 8, 1)

        self.info_open_loop_max_speed = self.create_spin_box()
        self.add_widget(layout, self.info_open_loop_max_speed, 9, 1)

        self.info_closed_loop_max_speed = self.create_spin_box()
        self.add_widget(layout, self.info_closed_loop_max_speed, 10, 1)

        self.info_min_pid_limit = self.create_spin_box()
        self.add_widget(layout, self.info_min_pid_limit, 11, 1)

        self.info_max_pid_limit = self.create_spin_box()
        self.add_widget(layout, self.info_max_pid_limit, 12, 1)

        # -- Buttons Send/Read -- #
        button_read_settings = QPushButton("Read Settings")
        button_read_settings.clicked.connect(self.read_settings_general_settings_tab)
        layout.addWidget(button_read_settings, 13, 2)

        button_write_settings = QPushButton("Write settings")
        button_write_settings.clicked.connect(self.write_settings_general_settings_tab)
        layout.addWidget(button_write_settings, 13, 3)

    def add_label(self, layout, text, row, col):
        label = QLabel(text)
        layout.addWidget(label, row, col)
        return label

    def add_widget(self, layout, widget, row, col):
        layout.addWidget(widget, row, col)

    def create_spin_box(self):
        spin_box = QDoubleSpinBox()
        spin_box.setReadOnly(False)
        spin_box.setRange(-100, 100)
        spin_box.setDecimals(3)
        return spin_box

    def create_checkbox(self):
        checkbox = QCheckBox()
        return checkbox

    def read_settings_general_settings_tab(self):
        self.info_yaw_offset.setValue(float(self.jsonHandlerObj.yaw_offset_list[-1]))
        self.info_aar_offset.setValue(float(self.jsonHandlerObj.aar_offset_list[-1]))
        if (self.jsonHandlerObj.control_instability_protection_list[-1] == 1):
            self.checkbox_control_instability_protection.setChecked(True)
        else:
            self.checkbox_control_instability_protection.setChecked(False)
        self.info_min_voltage.setValue(float(self.jsonHandlerObj.min_voltage_list[-1]))
        self.info_max_voltage.setValue(float(self.jsonHandlerObj.max_voltage_list[-1]))
        self.info_open_loop_max_speed.setValue(float(self.jsonHandlerObj.open_loop_max_speed_list[-1]))
        self.info_closed_loop_max_speed.setValue(float(self.jsonHandlerObj.closed_loop_max_speed_list[-1]))
        self.info_min_pid_limit.setValue(float(self.jsonHandlerObj.min_PID_limit_list[-1]))
        self.info_max_pid_limit.setValue(float(self.jsonHandlerObj.max_PID_limit_list[-1]))

    def write_settings_general_settings_tab(self):
        self.jsonHandlerObj.json_to_send_general_settings["General settings"]["Write general settings"] = 1
        self.jsonHandlerObj.json_to_send_general_settings["General settings"]["yawOffset"] = self.info_yaw_offset.value()
        self.jsonHandlerObj.json_to_send_general_settings["General settings"]["AAROffset"] = self.info_aar_offset.value()
        if (self.checkbox_control_instability_protection.isChecked() == True):
            self.jsonHandlerObj.json_to_send_general_settings["General settings"]["controlInstabilityProtection"] = 1
        else:
            self.jsonHandlerObj.json_to_send_general_settings["General settings"]["controlInstabilityProtection"] = 0
        self.jsonHandlerObj.json_to_send_general_settings["General settings"]["minVoltage"] = self.info_min_voltage.value()
        self.jsonHandlerObj.json_to_send_general_settings["General settings"]["maxVoltage"] = self.info_max_voltage.value()
        self.jsonHandlerObj.json_to_send_general_settings["General settings"]["openLoopMaxSpeed"] = self.info_open_loop_max_speed.value()
        self.jsonHandlerObj.json_to_send_general_settings["General settings"]["closedLoopMaxSpeed"] = self.info_closed_loop_max_speed.value()
        self.jsonHandlerObj.json_to_send_general_settings["General settings"]["minPIDLimit"] = self.info_min_pid_limit.value()
        self.jsonHandlerObj.json_to_send_general_settings["General settings"]["maxPIDLimit"] = self.info_max_pid_limit.value()
        self.serial_thread.write_to_serial(json.dumps(self.jsonHandlerObj.json_to_send_general_settings))
        self.jsonHandlerObj.json_to_send_general_settings["General settings"]["Write general settings"] = 0

    # -- Methods Tab 3 -- #
    def create_tab3_control_settings_ui(self):
        """
        Creates UI elements for the 'Control settings' tab.

        Args:
            None

        Returns:
            None
        """
        layout = QGridLayout(self.tab3)
        # -- Offsets -- #
        # Labels
        layout.addWidget(QLabel("<b>Prefilter</b>"), 0, 0)
        label_prefilter_numerator = QLabel("Numerator")
        label_prefilter_denominator = QLabel("Denominator")
        layout.addWidget(label_prefilter_numerator, 1, 0)
        layout.addWidget(label_prefilter_denominator, 2, 0)
        # Numerator QDoubleSpinBox
        self.info_prefilter_numerator_arg1 = QDoubleSpinBox()
        self.info_prefilter_numerator_arg1.setReadOnly(False)
        self.info_prefilter_numerator_arg1.setRange(-100, 100)
        self.info_prefilter_numerator_arg1.setDecimals(3)
        layout.addWidget(self.info_prefilter_numerator_arg1, 1, 1)
        self.info_prefilter_numerator_arg2 = QDoubleSpinBox()
        self.info_prefilter_numerator_arg2.setReadOnly(False)
        self.info_prefilter_numerator_arg2.setRange(-100, 100)
        self.info_prefilter_numerator_arg2.setDecimals(3)
        layout.addWidget(self.info_prefilter_numerator_arg2, 1, 2)
        self.info_prefilter_numerator_arg3 = QDoubleSpinBox()
        self.info_prefilter_numerator_arg3.setReadOnly(False)
        self.info_prefilter_numerator_arg3.setRange(-100, 100)
        self.info_prefilter_numerator_arg3.setDecimals(3)
        layout.addWidget(self.info_prefilter_numerator_arg3, 1, 3)
        self.info_prefilter_numerator_arg4 = QDoubleSpinBox()
        self.info_prefilter_numerator_arg4.setReadOnly(False)
        self.info_prefilter_numerator_arg4.setRange(-100, 100)
        self.info_prefilter_numerator_arg4.setDecimals(3)
        layout.addWidget(self.info_prefilter_numerator_arg4, 1, 4)
        # Denominator QDoubleSpinBox
        self.info_prefilter_denominator_arg1 = QDoubleSpinBox()
        self.info_prefilter_denominator_arg1.setReadOnly(False)
        self.info_prefilter_denominator_arg1.setRange(-100, 100)
        self.info_prefilter_denominator_arg1.setDecimals(3)
        layout.addWidget(self.info_prefilter_denominator_arg1, 2, 1)
        self.info_prefilter_denominator_arg2 = QDoubleSpinBox()
        self.info_prefilter_denominator_arg2.setReadOnly(False)
        self.info_prefilter_denominator_arg2.setRange(-100, 100)
        self.info_prefilter_denominator_arg2.setDecimals(3)
        layout.addWidget(self.info_prefilter_denominator_arg2, 2, 2)

        # -- Filter 1 -- #
        # Labels
        layout.addWidget(QLabel("<b>Filter 1</b>"), 3, 0)
        label_filter_1_numerator = QLabel("Numerator")
        label_filter_1_denominator = QLabel("Denominator")
        layout.addWidget(label_filter_1_numerator, 4, 0)
        layout.addWidget(label_filter_1_denominator, 5, 0)
        # Numerator LineEdit
        self.info_filter_1_numerator_arg1 = QDoubleSpinBox()
        self.info_filter_1_numerator_arg1.setReadOnly(False)
        self.info_filter_1_numerator_arg1.setRange(-100, 100)
        self.info_filter_1_numerator_arg1.setDecimals(3)
        layout.addWidget(self.info_filter_1_numerator_arg1, 4, 1)
        self.info_filter_1_numerator_arg2 = QDoubleSpinBox()
        self.info_filter_1_numerator_arg2.setReadOnly(False)
        self.info_filter_1_numerator_arg2.setRange(-100, 100)
        self.info_filter_1_numerator_arg2.setDecimals(3)
        layout.addWidget(self.info_filter_1_numerator_arg2, 4, 2)
        self.info_filter_1_numerator_arg3 = QDoubleSpinBox()
        self.info_filter_1_numerator_arg3.setReadOnly(False)
        self.info_filter_1_numerator_arg3.setRange(-100, 100)
        self.info_filter_1_numerator_arg3.setDecimals(3)
        layout.addWidget(self.info_filter_1_numerator_arg3, 4, 3)
        self.info_filter_1_numerator_arg4 = QDoubleSpinBox()
        self.info_filter_1_numerator_arg4.setReadOnly(False)
        self.info_filter_1_numerator_arg4.setRange(-100, 100)
        self.info_filter_1_numerator_arg4.setDecimals(3)
        layout.addWidget(self.info_filter_1_numerator_arg4, 4, 4)
        # Denominator LineEdit
        self.info_filter_1_denominator_arg1 = QDoubleSpinBox()
        self.info_filter_1_denominator_arg1.setReadOnly(False)
        self.info_filter_1_denominator_arg1.setRange(-100, 100)
        self.info_filter_1_denominator_arg1.setDecimals(3)
        layout.addWidget(self.info_filter_1_denominator_arg1, 5, 1)
        self.info_filter_1_denominator_arg2 = QDoubleSpinBox()
        self.info_filter_1_denominator_arg2.setReadOnly(False)
        self.info_filter_1_denominator_arg2.setRange(-100, 100)
        self.info_filter_1_denominator_arg2.setDecimals(3)
        layout.addWidget(self.info_filter_1_denominator_arg2, 5, 2)

        # -- Filter 2 -- #
        # Labels
        layout.addWidget(QLabel("<b>Filter 2</b>"), 6, 0)
        label_filter_2_numerator = QLabel("Numerator")
        label_filter_2_denominator = QLabel("Denominator")
        layout.addWidget(label_filter_2_numerator, 7, 0)
        layout.addWidget(label_filter_2_denominator, 8, 0)
        # Numerator LineEdit
        self.info_filter_2_numerator_arg1 = QDoubleSpinBox()
        self.info_filter_2_numerator_arg1.setReadOnly(False)
        self.info_filter_2_numerator_arg1.setRange(-100, 100)
        self.info_filter_2_numerator_arg1.setDecimals(3)
        layout.addWidget(self.info_filter_2_numerator_arg1, 7, 1)
        self.info_filter_2_numerator_arg2 = QDoubleSpinBox()
        self.info_filter_2_numerator_arg2.setReadOnly(False)
        self.info_filter_2_numerator_arg2.setRange(-100, 100)
        self.info_filter_2_numerator_arg2.setDecimals(3)
        layout.addWidget(self.info_filter_2_numerator_arg2, 7, 2)
        # Denominator LineEdit
        self.info_filter_2_denominator_arg1 = QDoubleSpinBox()
        self.info_filter_2_denominator_arg1.setReadOnly(False)
        self.info_filter_2_denominator_arg1.setRange(-100, 100)
        self.info_filter_2_denominator_arg1.setDecimals(3)
        layout.addWidget(self.info_filter_2_denominator_arg1, 8, 1)

        # -- Filter 3 -- #
        # Labels
        layout.addWidget(QLabel("<b>Filter 3</b>"), 9, 0)
        label_filter_3_numerator = QLabel("Numerator")
        label_filter_3_denominator = QLabel("Denominator")
        layout.addWidget(label_filter_3_numerator, 10, 0)
        layout.addWidget(label_filter_3_denominator, 11, 0)
        # Numerator LineEdit
        self.info_filter_3_numerator_arg1 = QDoubleSpinBox()
        self.info_filter_3_numerator_arg1.setReadOnly(False)
        self.info_filter_3_numerator_arg1.setRange(-100, 100)
        self.info_filter_3_numerator_arg1.setDecimals(3)
        layout.addWidget(self.info_filter_3_numerator_arg1, 10, 1)
        self.info_filter_3_numerator_arg2 = QDoubleSpinBox()
        self.info_filter_3_numerator_arg2.setReadOnly(False)
        self.info_filter_3_numerator_arg2.setRange(-100, 100)
        self.info_filter_3_numerator_arg2.setDecimals(3)
        layout.addWidget(self.info_filter_3_numerator_arg2, 10, 2)
        # Denominator LineEdit
        self.info_filter_3_denominator_arg1 = QDoubleSpinBox()
        self.info_filter_3_denominator_arg1.setReadOnly(False)
        self.info_filter_3_denominator_arg1.setRange(-100, 100)
        self.info_filter_3_denominator_arg1.setDecimals(3)
        layout.addWidget(self.info_filter_3_denominator_arg1, 11, 1)

        # -- Hysteresis compensator -- #
        # Labels
        layout.addWidget(QLabel("<b>Hysteresis compensator</b>"), 12, 0)
        label_hysteresis_compensation = QLabel("Hysteresis compensation")
        layout.addWidget(label_hysteresis_compensation, 13, 0)
        label_compensation_offset = QLabel("Compensation offset (urad)")
        layout.addWidget(label_compensation_offset, 14, 0)
        label_quadratic_parameters = QLabel("Quadratic parameters")
        layout.addWidget(label_quadratic_parameters, 15, 0)
        label_f_parameters = QLabel("f parameters")
        layout.addWidget(label_f_parameters, 16, 0)
        label_k_parameters = QLabel("k parameters")
        layout.addWidget(label_k_parameters, 17, 0)
        # Checkbox
        self.checkbox_hysteresis_compensation = QCheckBox()
        layout.addWidget(self.checkbox_hysteresis_compensation, 13, 1, 1, 2)
        # SpinBoxes
        self.info_compensation_offset_arg1 = QDoubleSpinBox()
        self.info_compensation_offset_arg1.setReadOnly(False)
        self.info_compensation_offset_arg1.setRange(-100, 100)
        self.info_compensation_offset_arg1.setDecimals(3)
        layout.addWidget(self.info_compensation_offset_arg1, 14, 1)
        self.info_quadratic_parameters_arg1 = QDoubleSpinBox()
        self.info_quadratic_parameters_arg1.setReadOnly(False)
        self.info_quadratic_parameters_arg1.setRange(-100, 100)
        self.info_quadratic_parameters_arg1.setDecimals(3)
        layout.addWidget(self.info_quadratic_parameters_arg1, 15, 1)
        self.info_quadratic_parameters_arg2 = QDoubleSpinBox()
        self.info_quadratic_parameters_arg2.setReadOnly(False)
        self.info_quadratic_parameters_arg2.setRange(-100, 100)
        self.info_quadratic_parameters_arg2.setDecimals(3)
        layout.addWidget(self.info_quadratic_parameters_arg2, 15, 2)
        self.info_f_parameters_arg1 = QDoubleSpinBox()
        self.info_f_parameters_arg1.setReadOnly(False)
        self.info_f_parameters_arg1.setRange(-100, 100)
        self.info_f_parameters_arg1.setDecimals(3)
        layout.addWidget(self.info_f_parameters_arg1, 16, 1)
        self.info_f_parameters_arg2 = QDoubleSpinBox()
        self.info_f_parameters_arg2.setReadOnly(False)
        self.info_f_parameters_arg2.setRange(-100, 100)
        self.info_f_parameters_arg2.setDecimals(3)
        layout.addWidget(self.info_f_parameters_arg2, 16, 2)
        self.info_k_parameters_arg1 = QDoubleSpinBox()
        self.info_k_parameters_arg1.setReadOnly(False)
        self.info_k_parameters_arg1.setRange(-100, 100)
        self.info_k_parameters_arg1.setDecimals(3)
        layout.addWidget(self.info_k_parameters_arg1, 17, 1)
        self.info_k_parameters_arg2 = QDoubleSpinBox()
        self.info_k_parameters_arg2.setReadOnly(False)
        self.info_k_parameters_arg2.setRange(-100, 100)
        self.info_k_parameters_arg2.setDecimals(3)
        layout.addWidget(self.info_k_parameters_arg2, 17, 2)

        # -- Buttons Send/Read -- #
        button_read_settings = QPushButton("Read Settings")
        button_read_settings.clicked.connect(self.read_settings_control_settings_tab)
        layout.addWidget(button_read_settings, 18, 4)

        button_write_settings = QPushButton("Write settings")
        button_write_settings.clicked.connect(self.write_settings_control_settings_tab)
        layout.addWidget(button_write_settings, 18, 5)
    
    def read_settings_control_settings_tab(self):
        # read prefilter
        self.info_prefilter_numerator_arg1.setValue(float(self.jsonHandlerObj.prefilter_numerator_arg1[-1]))
        self.info_prefilter_numerator_arg2.setValue(float(self.jsonHandlerObj.prefilter_numerator_arg2[-1]))
        self.info_prefilter_numerator_arg3.setValue(float(self.jsonHandlerObj.prefilter_numerator_arg3[-1]))
        self.info_prefilter_numerator_arg4.setValue(float(self.jsonHandlerObj.prefilter_numerator_arg4[-1]))
        self.info_prefilter_denominator_arg1.setValue(float(self.jsonHandlerObj.prefilter_denominator_arg1[-1]))
        self.info_prefilter_denominator_arg2.setValue(float(self.jsonHandlerObj.prefilter_denominator_arg2[-1]))
        # read filter 1
        self.info_filter_1_numerator_arg1.setValue(float(self.jsonHandlerObj.filter_1_numerator_arg1[-1]))
        self.info_filter_1_numerator_arg2.setValue(float(self.jsonHandlerObj.filter_1_numerator_arg2[-1]))
        self.info_filter_1_numerator_arg3.setValue(float(self.jsonHandlerObj.filter_1_numerator_arg3[-1]))
        self.info_filter_1_numerator_arg4.setValue(float(self.jsonHandlerObj.filter_1_numerator_arg4[-1]))
        self.info_filter_1_denominator_arg1.setValue(float(self.jsonHandlerObj.filter_1_denominator_arg1[-1]))
        self.info_filter_1_denominator_arg2.setValue(float(self.jsonHandlerObj.filter_1_denominator_arg2[-1]))
        # read filter 2
        self.info_filter_2_numerator_arg1.setValue(float(self.jsonHandlerObj.filter_2_numerator_arg1[-1]))
        self.info_filter_2_numerator_arg2.setValue(float(self.jsonHandlerObj.filter_2_numerator_arg2[-1]))
        self.info_filter_2_denominator_arg1.setValue(float(self.jsonHandlerObj.filter_2_denominator_arg1[-1]))
        # read filter 3
        self.info_filter_3_numerator_arg1.setValue(float(self.jsonHandlerObj.filter_3_numerator_arg1[-1]))
        self.info_filter_3_numerator_arg2.setValue(float(self.jsonHandlerObj.filter_3_numerator_arg2[-1]))
        self.info_filter_3_denominator_arg1.setValue(float(self.jsonHandlerObj.filter_3_denominator_arg1[-1]))
        # read hysteresis compensation
        if (self.jsonHandlerObj.hysteresis_compensation_list[-1] == 1):
            self.checkbox_hysteresis_compensation.setChecked(True)
        else:
            self.checkbox_hysteresis_compensation.setChecked(False)
        # read compensation offset
        self.info_compensation_offset_arg1.setValue(float(self.jsonHandlerObj.compensation_offset_list[-1]))
        # read quadratic parameters
        self.info_quadratic_parameters_arg1.setValue(float(self.jsonHandlerObj.quadratic_parameters_arg1_list[-1]))
        self.info_quadratic_parameters_arg2.setValue(float(self.jsonHandlerObj.quadratic_parameters_arg2_list[-1]))
        # read f parameters
        self.info_f_parameters_arg1.setValue(float(self.jsonHandlerObj.f_parameters_arg1_list[-1]))
        self.info_f_parameters_arg2.setValue(float(self.jsonHandlerObj.f_parameters_arg2_list[-1]))
        # read k parameters
        self.info_k_parameters_arg1.setValue(float(self.jsonHandlerObj.k_parameters_arg1_list[-1]))
        self.info_k_parameters_arg2.setValue(float(self.jsonHandlerObj.k_parameters_arg2_list[-1]))

    def write_settings_control_settings_tab(self):
        # write prefilter
        self.jsonHandlerObj.json_to_send_control_settings["Control settings"]["Write control settings"] = 1
        self.jsonHandlerObj.json_to_send_control_settings["Control settings"]["prefilterNumerator"][0] = self.info_prefilter_numerator_arg1.value()
        self.jsonHandlerObj.json_to_send_control_settings["Control settings"]["prefilterNumerator"][1] = self.info_prefilter_numerator_arg2.value()
        self.jsonHandlerObj.json_to_send_control_settings["Control settings"]["prefilterNumerator"][2] = self.info_prefilter_numerator_arg3.value()
        self.jsonHandlerObj.json_to_send_control_settings["Control settings"]["prefilterNumerator"][3] = self.info_prefilter_numerator_arg4.value()
        self.jsonHandlerObj.json_to_send_control_settings["Control settings"]["prefilterDenominator"][0] = self.info_prefilter_denominator_arg1.value()
        self.jsonHandlerObj.json_to_send_control_settings["Control settings"]["prefilterDenominator"][1] = self.info_prefilter_denominator_arg2.value()
        # write filter 1
        self.jsonHandlerObj.json_to_send_control_settings["Control settings"]["filter1Numerator"][0] = self.info_filter_1_numerator_arg1.value()
        self.jsonHandlerObj.json_to_send_control_settings["Control settings"]["filter1Numerator"][1] = self.info_filter_1_numerator_arg2.value()
        self.jsonHandlerObj.json_to_send_control_settings["Control settings"]["filter1Numerator"][2] = self.info_filter_1_numerator_arg3.value()
        self.jsonHandlerObj.json_to_send_control_settings["Control settings"]["filter1Numerator"][3] = self.info_filter_1_numerator_arg4.value()
        self.jsonHandlerObj.json_to_send_control_settings["Control settings"]["filter1Denominator"][0] = self.info_filter_1_denominator_arg1.value()
        self.jsonHandlerObj.json_to_send_control_settings["Control settings"]["filter1Denominator"][1] = self.info_filter_1_denominator_arg2.value()
        # write filter 2
        self.jsonHandlerObj.json_to_send_control_settings["Control settings"]["filter2Numerator"][0] = self.info_filter_2_numerator_arg1.value()
        self.jsonHandlerObj.json_to_send_control_settings["Control settings"]["filter2Numerator"][1] = self.info_filter_2_numerator_arg2.value()
        self.jsonHandlerObj.json_to_send_control_settings["Control settings"]["filter2Denominator"]= self.info_filter_2_denominator_arg1.value()
        # write filter 3
        self.jsonHandlerObj.json_to_send_control_settings["Control settings"]["filter3Numerator"][0] = self.info_filter_3_numerator_arg1.value()
        self.jsonHandlerObj.json_to_send_control_settings["Control settings"]["filter3Numerator"][1] = self.info_filter_3_numerator_arg2.value()
        self.jsonHandlerObj.json_to_send_control_settings["Control settings"]["filter3Denominator"] = self.info_filter_3_denominator_arg1.value()
        # write hysteresis compensation
        if (self.checkbox_hysteresis_compensation.isChecked() == True):
            self.jsonHandlerObj.json_to_send_control_settings["Control settings"]["hysteresisCompensation"] = 1
        else:
            self.jsonHandlerObj.json_to_send_control_settings["Control settings"]["hysteresisCompensation"] = 0
        # write compensation offset
        self.jsonHandlerObj.json_to_send_control_settings["Control settings"]["compensationOffset"] = self.info_compensation_offset_arg1.value()
        # write quadratic parameters
        self.jsonHandlerObj.json_to_send_control_settings["Control settings"]["quadraticParameters"][0] = self.info_quadratic_parameters_arg1.value()
        self.jsonHandlerObj.json_to_send_control_settings["Control settings"]["quadraticParameters"][1] = self.info_quadratic_parameters_arg2.value()
        # write f parameters
        self.jsonHandlerObj.json_to_send_control_settings["Control settings"]["fParameters"][0] = self.info_f_parameters_arg1.value()
        self.jsonHandlerObj.json_to_send_control_settings["Control settings"]["fParameters"][1] = self.info_f_parameters_arg2.value()
        # write k parameters
        self.jsonHandlerObj.json_to_send_control_settings["Control settings"]["kParameters"][0] = self.info_k_parameters_arg1.value()
        self.jsonHandlerObj.json_to_send_control_settings["Control settings"]["kParameters"][1] = self.info_k_parameters_arg2.value()
        # send json
        #self.serial_thread.write_to_serial(json.dumps(self.jsonHandlerObj.json_to_send_control_settings))
        #self.jsonHandlerObj.json_to_send_control_settings["Control settings"]["Write control settings"] = 0
    
    def create_tab4_expert_procedures_ui(self):
        """
        Creates UI elements for the 'Expert procedures' tab.

        Args:
            None

        Returns:
            None
        """
        layout = QGridLayout(self.tab4)
        # -- Profile motion -- #
        layout.addWidget(QLabel("<b>Profile motion</b>"), 0, 0)
        label_waveform_id = QLabel("Waveform id")
        layout.addWidget(label_waveform_id, 1, 0)
        self.waveform_id = QSpinBox()
        self.waveform_id.setRange(0, 100)
        layout.addWidget(self.waveform_id, 1, 1)
        # -- Start/Stop motion -- #
        self.button_start_motion_profile_motion = QPushButton("Start motion")
        self.button_start_motion_profile_motion.clicked.connect(self.start_motion_profile_motion)
        layout.addWidget(self.button_start_motion_profile_motion, 2, 0)
        self.button_stop_motion_profile_motion = QPushButton("Stop motion")
        self.button_stop_motion_profile_motion.clicked.connect(self.stop_motion_profile_motion)
        layout.addWidget(self.button_stop_motion_profile_motion, 2, 1)
        
        # -- Ramp cycles -- #
        layout.addWidget(QLabel("<b>Ramp cycles</b>"), 3, 0)
        label_number_cycles = QLabel("Number cycles")
        layout.addWidget(label_number_cycles, 4, 0)
        label_ramp_rate = QLabel("Ramp rate")
        layout.addWidget(label_ramp_rate, 5, 0)
        self.number_cycles = QSpinBox()
        self.number_cycles.setRange(0, 100)
        layout.addWidget(self.number_cycles, 4, 1)
        self.spinbox_ramp_rate = QDoubleSpinBox()
        self.spinbox_ramp_rate.setRange(-100, 100)
        layout.addWidget(self.spinbox_ramp_rate, 5, 1)
        # -- Start/Stop motion -- #
        self.button_start_motion_profile_motion = QPushButton("Start motion")
        self.button_start_motion_profile_motion.clicked.connect(self.start_motion_ramp_cycles)
        layout.addWidget(self.button_start_motion_profile_motion, 6, 0)
        self.button_stop_motion_profile_motion = QPushButton("Stop motion")
        self.button_stop_motion_profile_motion.clicked.connect(self.stop_motion_ramp_cycles)
        layout.addWidget(self.button_stop_motion_profile_motion, 6, 1)
        
        # -- Logging -- #
        layout.addWidget(QLabel("<b>Logging</b>"), 7, 0)
        layout.addWidget(QLabel("Logging"), 8, 0)
        self.button_logging = QPushButton("Start logging")
        self.button_logging.clicked.connect(self.start_logging)
        layout.addWidget(self.button_logging, 8, 1)
        button_save_settings = QPushButton("Save settings")
        button_save_settings.clicked.connect(self.button_save_settings_clicked)
        layout.addWidget(button_save_settings, 9, 1)
              
    def start_logging(self):
        state = self.combo_box_mode.currentText()
        if state == "Closed Loop": 
            QMessageBox.information(self, "Notification", "Please open the loop to start the logging.")
            return
        else: # open loop
            #QMessageBox.information(self, "Notification", "Logging Started.")
            self.jsonHandlerObj.json_to_send_expert_precedures["Expert procedures"]["Logging"]  = 1
            # send json
            self.serial_thread.write_to_serial(json.dumps(self.jsonHandlerObj.json_to_send_expert_precedures))
            self.jsonHandlerObj.json_to_send_expert_precedures["Expert procedures"]["Logging"] = 0
        
    def button_save_settings_clicked(self):
        current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename_ControlsTab = f"Controls_Tab_{current_datetime}.json"
        filename_GeneralSettingsTab = f"General_Settings_Tab_{current_datetime}.json"
        filename_ControlSettingsTab = f"Control_Settings_Tab_{current_datetime}.json"
        filename_ExpertProceduresTab = f"Expert_Preocedures_Tab_{current_datetime}.json"
        with open(filename_ControlsTab, "w") as json_file:
            json.dump(self.jsonHandlerObj.json_to_send_controls, json_file, indent=4)
            
        with open(filename_GeneralSettingsTab, "w") as json_file:
            json.dump(self.jsonHandlerObj.json_to_send_general_settings, json_file, indent=4)
            
        with open(filename_ControlSettingsTab, "w") as json_file:
            json.dump(self.jsonHandlerObj.json_to_send_control_settings, json_file, indent=4)
            
        with open(filename_ExpertProceduresTab, "w") as json_file:
            json.dump(self.jsonHandlerObj.json_to_send_expert_precedures, json_file, indent=4)
    
    def start_motion_profile_motion(self):
        self.jsonHandlerObj.json_to_send_expert_precedures["Expert procedures"]["Profile motion Start"] = 1
        self.jsonHandlerObj.json_to_send_expert_precedures["Expert procedures"]["Profile motion Stop"]  = 0
        self.jsonHandlerObj.json_to_send_expert_precedures["Expert procedures"]["waveformID"]  = self.waveform_id.value()
        # send json
        self.serial_thread.write_to_serial(json.dumps(self.jsonHandlerObj.json_to_send_expert_precedures))
        self.jsonHandlerObj.json_to_send_expert_precedures["Expert procedures"]["Profile motion Start"] = 0
        self.serial_thread.write_to_serial(json.dumps(self.jsonHandlerObj.json_to_send_expert_precedures))
        
    def stop_motion_profile_motion(self):
        self.jsonHandlerObj.json_to_send_expert_precedures["Expert procedures"]["Profile motion Start"] = 0
        self.jsonHandlerObj.json_to_send_expert_precedures["Expert procedures"]["Profile motion Stop"]  = 1
        self.jsonHandlerObj.json_to_send_expert_precedures["Expert procedures"]["waveform id"]  = self.waveform_id.value()
        # send json
        self.serial_thread.write_to_serial(json.dumps(self.jsonHandlerObj.json_to_send_expert_precedures))
        self.jsonHandlerObj.json_to_send_expert_precedures["Expert procedures"]["Profile motion Stop"]  = 0
        self.serial_thread.write_to_serial(json.dumps(self.jsonHandlerObj.json_to_send_expert_precedures))
        
    def start_motion_ramp_cycles(self):
       self.jsonHandlerObj.json_to_send_expert_precedures["Expert procedures"]["Ramp cycles motion Start"] = 1
       self.jsonHandlerObj.json_to_send_expert_precedures["Expert procedures"]["Ramp cycles motion Stop"]  = 0
       self.jsonHandlerObj.json_to_send_expert_precedures["Expert procedures"]["numberCycles"]  = self.number_cycles.value()
       self.jsonHandlerObj.json_to_send_expert_precedures["Expert procedures"]["rampRate"]      = self.spinbox_ramp_rate.value()
       # send json
       self.serial_thread.write_to_serial(json.dumps(self.jsonHandlerObj.json_to_send_expert_precedures))
       self.jsonHandlerObj.json_to_send_expert_precedures["Expert procedures"]["Ramp cycles motion Start"] = 0
       self.serial_thread.write_to_serial(json.dumps(self.jsonHandlerObj.json_to_send_expert_precedures))
        
    def stop_motion_ramp_cycles(self):
       self.jsonHandlerObj.json_to_send_expert_precedures["Expert procedures"]["Ramp cycles motion Start"] = 0
       self.jsonHandlerObj.json_to_send_expert_precedures["Expert procedures"]["Ramp cycles motion Stop"]  = 1
       self.jsonHandlerObj.json_to_send_expert_precedures["Expert procedures"]["numberCycles"]  = self.number_cycles.value()
       self.jsonHandlerObj.json_to_send_expert_precedures["Expert procedures"]["rampRate"]      = self.spinbox_ramp_rate.value()
       # send json
       self.serial_thread.write_to_serial(json.dumps(self.jsonHandlerObj.json_to_send_expert_precedures))
       self.jsonHandlerObj.json_to_send_expert_precedures["Expert procedures"]["Ramp cycles motion Stop"]  = 0
       self.serial_thread.write_to_serial(json.dumps(self.jsonHandlerObj.json_to_send_expert_precedures))
    
    def handle_serial_data(self, data):
        """
        Handles incoming serial data.
        
        Args:
            data (bytes): The serial data received.
        
        Returns:
            None
        
        This method parses the JSON string data, updates the UI elements with the latest values from the JSON data.
        """
        self.jsonHandlerObj.parse_json_string(str(data))
        self.info_controller_state.setText(str(self.jsonHandlerObj.controller_state_list[-1]))
        self.info_yaw_angle.setText(str(self.jsonHandlerObj.yaw_angle_list[-1]))
        self.info_yaw_std.setText(str(self.jsonHandlerObj.yaw_std_list[-1]))
        self.set_led_head_error_1_color(str(self.jsonHandlerObj.error_axis1_list[-1]))
        self.set_led_head_error_2_color(str(self.jsonHandlerObj.error_axis2_list[-1]))

    def closeEvent(self, event):
        self.disconnect_serial()
        event.accept()

