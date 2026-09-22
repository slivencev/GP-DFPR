# v14 observation-model package

OBSERVATION_MODEL_RU.md defines the acquisition design, measurement/prediction distinction and error assumptions. evidence.py implements only a gate for already-supplied evidence and basic bound/quantile arithmetic. It does not connect to a gNB, create counterfactual measurements, estimate valid hard bounds, or supply adaptive joint statistical coverage. Merely supplying an assumption_ref string does not prove a bound; upstream validation is required.

Run `python test_evidence.py`. Nine tests use explicit synthetic assumptions and check only interface semantics. No new radio experiment is claimed; v3–v12 retain their original idealized observation model and are not retrospectively relabeled as real measurement validation.

Suggested acquisition record: observation_id; action/component identifiers; active configuration; context; source type (telemetry/probe/model); sensor and software version; measurement-window start/end; observation and receipt timestamps; measured fields with units; prediction model and calibration versions; supported domain; interval and bound type; risk level if applicable; model/drift assumptions; affected alternatives; latency; measurement resource cost; probe-induced interference/load. Reusing one observation for several alternatives must not be charged as several independent measurements or treated as independent statistical evidence.

Source URLs and verified limitations are embedded in the design report. EXISTING_EXTERNAL_CALIBRATION.json is an unchanged copy of the earlier v2 calibration summary and explicitly lacks a coverage guarantee; it is not a calibration for inactive actions.
