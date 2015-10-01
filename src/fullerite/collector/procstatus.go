package collector

import (
	"fullerite/metric"

	l "github.com/Sirupsen/logrus"
)

// ProcStatus collector type
type ProcStatus struct {
	baseCollector
	processName string
}

// ProcessName returns ProcStatus collectors process name
func (ps ProcStatus) ProcessName() string {
	return ps.processName
}

// NewProcStatus creates a new Test collector.
func NewProcStatus(channel chan metric.Metric, initialInterval int, log *l.Entry) *ProcStatus {
	ps := new(ProcStatus)

	ps.log = log
	ps.channel = channel
	ps.interval = initialInterval

	ps.name = "ProcStatus"
	ps.processName = ""

	return ps
}

// Configure this takes a dictionary of values with which the handler can configure itself
func (ps *ProcStatus) Configure(configMap map[string]interface{}) {
	if processName, exists := configMap["processName"]; exists == true {
		ps.processName = processName.(string)
	}
	ps.configureCommonParams(configMap)
}