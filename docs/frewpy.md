# Frewpy Information
> This document contains information on the available methods within the frewLib COM object, FrewComAuto interface. Other available documentation is contained within the Oasys Frew program files.

## Model commands
`Show()` -> returns: none

`Open(BSTR sPathName)` -> returns: short* retCode

> *To open an existing Frew model*

`Analyse(short iStage)` -> returns: short* retCode

> *To run the analysis on the Frew model*

`DeleteResults()` -> returns: short* retCode

> *To delete any pre-existing results within a Frew model if opened or if between iterations*

`Save()` -> returns: short* retCode

`SaveAs(BSTR sPathName)` ->`returns: short* retCode

`Close()` -> returns: short* retCode

`SetAnalysisMethod()`

---

## Wall
### Get information
`GetNumNodes()` -> returns: short* psNumNodes

`GetNodeLevel(short index)` -> returns: double* retVal

`GetNodeDisp(short index, short iStage)` -> returns: double* retVal

`GetNodeBending`

`GetNodeShear`

`GetWallEI`

`GetWallBaseNode`

### Set information
`SetWallEI`

---

## Struts
### Get information
`GetStrutBendingAtNode`

`GetStrutShearAtNode`

`GetNumStruts`

`GetStrutPrestress`

`GetStrutStiffness`

`GetStrutAngle`

`GetStrutLeverArm`

`GetStrutStageIn`

`GetStrutStageOut`

`GetStrutForce`

`GetStrutHorizForce`

`GetStrutMoment`

`GetStrutMaxForce`

### Set information
`SetStrutPrestress`

`SetStrutStiffness`

`SetStrutAngle`

`SetStrutLeverArm`

`SetStrutStageIn`

`SetStrutStageOut`

---

## Springs

---

## Soil
### Get information
`GetNumMat`

`GetUnitWeight`

`GetEref`

`GetKref`

`GetPhi`

`GetCohesion`

`GetRefLevel`

`GetCGrad`

`GetEGrad`

`GetSoilZoneLeft`

`GetSoilZoneRight`

`GetEGradL`

`GetEGradR`

`GetEGroundL`

`GetEGroundR`

`GetNodeVeLeft`

`GetNodePeLeft`

`GetNodeVeRight`

`GetNodePeRight`

### Set information
`SetUnitWeight`

`SetEref`

`SetKref`

`SetPhi`

`SetCohesion`

`SetRefLevel`

`SetCGrad`

`SetEGrad`

`SetSoilZoneLeft`

`SetSoilZoneRight`

---

## Water
### Get information
`GetPorePressGradLeft`

`GetPorePressGradRight`

`GetWaterLevelLeft`

`GetWaterLevelRight`

`GetNodePPLeft`

`GetNodePPRight`

### Set information
`SetPorePressGradLeft`

`SetPorePressGradRight`

`SetWaterLevelLeft`

`SetWaterLevelRight`
