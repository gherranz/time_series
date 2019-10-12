"""
This file contains the all the constants to work correctly with the data frames
"""

# ======================================================
# COLUMN DEFINITION FOR DATA SET
# ======================================================
DATE = 'Date'
AXIS_X_POS = 'Axis_X_positionActualMCS_mm_d10000'
AXIS_Y_POS = 'Axis_Y_positionActualMCS_mm_d10000'
AXIS_Z_POS = 'Axis_Z_positionActualMCS_mm_d10000'
SPDL_C_POS = 'Spindle_C_deg'
SPDL_A_POS = 'Spindle_A_Deg'
PROGRAM_NAME = 'Cnc_Program_Name_RT'
PROG_BLK_NUM = 'Cnc_Program_BlockNumber_RT'
TOOL_NUMBER = 'Cnc_Tool_Number_RT'
AXIS_X_LOAD = 'Axis_X1_power_percent'
AXIS_Y_LOAD = 'Axis_Y_power_percent'
AXIS_Z_LOAD = 'Axis_Z_power_percent'
SPINDLE_LOAD = 'Spindle_Power_percent'
CHATTER_EXIST = 'System_DAS_Chatter'
SEVERIDAD_X = 'System_DAS_SeveridadActualX'
SEVERIDAD_Y = 'System_DAS_SeveridadActualY'
AXIS_OVERRIDE = 'Cnc_Override_Axis'
SPINDLE_OVERRIDE = 'Cnc_Override_Spindle'
CYCLE_IS_ON = 'Cnc_IsCycleOn_RT'
OPERATION_CODE = 'CNC_Operation_Code'


# ======================================================
# COLUMN DEFINITION FOR AUXILIAR HISTORICAL DATA SET
# ======================================================

PROGRAM_TOOL = 'prog-tool'
SEGMENT_BEGIN = 'segment_begin'
SEGMENT_END = 'segment_end'
OPERATION_ID_NUMBER = 'op_number'
YEAR_INDEX_LIMIT = 7804


# ======================================================
# CNC VARIABLE SETTINGS
# ======================================================

GLOBAL_SYMBOL = '\\PLC\\program\\symbol\\global\\'
ACTIVE_PROGRAM_NAME = r'\PLC\program\main'


# ======================================================
# CNC PROGRAM KEYWORDS
# ======================================================

TYP_TABLE_PATH = '\\TABLE\\TOOL\\T\\%s\\TYP'
KEYWORD_TCALL = ' TOOL CALL '
KEYWORD_ENDPGM = ' END PGM '
KEYWORD_MDI = '$MDI.H'


