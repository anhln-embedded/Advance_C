#ifndef DASHBOARDCONTROLLER_HPP
#define DASHBOARDCONTROLLER_HPP

#include "VehicleConfig.hpp"
// Forward declarations for the observer and other components
class Observer{
  public:
    virtual void update(
                        const uint16_t& speed,
                        const uint16_t& remaining_range,
                        const uint8_t& battery_level, 
                        const uint8_t& climate_temp,
                        const uint8_t& wind_level,
                        const string& turnSignal,
                        const string& drivemode, 
                        const bool& IsBraking,
                        const bool& IsAccelerating,
                        const bool& AC_status
                    ) = 0;
    ~Observer(){};
}; // Abstract base class for observers

class DashboardController {
public:
    // Constructor and Destructor
    DashboardController();
    ~DashboardController(){};

    // Data update method called by thread 1 for reading from csv database
    void updateData(const unordered_map<string, string>& newData);

    // Observer management methods
    void registerObserver(Observer* observer);
    void removeObserver(Observer* observer);
    void notifyObservers() const;

    // Getters for various system parameters
    uint16_t getSpeed() const{return speed;}
    string getDriveMode() const {return driveMode;}
    uint8_t getBatteryLevel() const {return batteryLevel;}
    uint16_t getRemainingRange() const {return remainingRange;}
    uint8_t getClimatStatus() const {return climateTemp;}
    uint8_t getWindLevel() const {return windlevel;}
    string getTurnSignal() const {return turnSignal;}
    bool getACstatus() const {return AC_status;}
    bool getBrakeStatus() const {return IsBraking;}
    bool getGasStatus() const {return IsAccelerating;}
    
private:
    // System parameters
    string driveMode,turnSignal;
    uint16_t speed,remainingRange;
    uint8_t batteryLevel,climateTemp,windlevel;
    bool AC_status,IsBraking,IsAccelerating;
    // List of observers
    vector<Observer*> observers;
};

#endif // DASHBOARDCONTROLLER_HPP

