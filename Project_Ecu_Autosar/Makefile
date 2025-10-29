# Compiler and flags
CC = gcc
LIBS = -pthread
CFLAGS = -Wall -g\
-I.\BSW\ECU_Abstraction\IoHwAb\
-I.\BSW\MCAL\
-I.\BSW\Services\
-I.\RTE\
-I.\SWC\
-I.
# Object directory
OBJDIR = bin
# Executable
TARGET = $(OBJDIR)/ecu

SRC = .\BSW\ECU_Abstraction\IoHwAb\IoHwAb_CurrentSensor.c \
.\BSW\ECU_Abstraction\IoHwAb\IoHwAb_MotorDriver.c \
.\BSW\ECU_Abstraction\IoHwAb\IoHwAb_RpmSensor.c \
.\BSW\ECU_Abstraction\IoHwAb\IoHwAb_TorqueSensor.c \
.\BSW\ECU_Abstraction\IoHwAb\IoHwAb_VoltageSensor.c \
.\BSW\MCAL\Adc.c \
.\BSW\MCAL\Can.c \
.\BSW\MCAL\Dio.c \
.\BSW\MCAL\Pwm.c \
.\BSW\Services\Dcm.c \
.\BSW\Services\Dem.c \
.\BSW\Services\Mem.c \
.\BSW\Services\Os.c \
.\BSW\Services\Os_Cfg.c \
.\BSW\Services\Pdu_Router.c \
.\demo.c \
.\main.c \
.\RTE\Rte.c \
.\SWC\Actuator_SWC.c \
.\SWC\Diagnostic_SWC.c \
.\SWC\EcuState_SWC.c \
.\SWC\EngineControl_SWC.c \
.\SWC\Sensor_SWC.c \
.\task.c 

# Object files
OBJ = $(SRC:%.c=$(OBJDIR)/%.o)

# Build executable
$(TARGET): $(OBJ)
	@echo "Linking all objects to create $(TARGET)..."
	$(CC) $(CFLAGS) $(LIBS) -o $(TARGET) $(OBJ)
	@echo "Build successful!"

# Compile object files
$(OBJDIR)/%.o: %.c
	@mkdir -p $(dir $@)
	$(CC) $(CFLAGS) -c $< -o $@
	@echo "Compiled: $<"

# Clean up
.PHONY: clean
clean:
	@echo "Cleaning up..."
	rm -rf $(OBJDIR)
	@echo "Clean done!"

# Run program
.PHONY: run
run: $(TARGET)
	@echo "Running program..."
	$(TARGET)
