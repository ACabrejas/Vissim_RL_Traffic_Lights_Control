<?xml version="1.0" encoding="UTF-8"?>
<sc version="201602" id="13" name="SC13" frequency="1" steps="0" defaultIntergreenMatrix="1" EPICSTimeHorizon="100000" EPICSLogLevel="1" interstagesUsingMinDurations="false" checkSum="412470259">
  <signaldisplays>
    <display id="1" name="Red" state="RED">
      <patterns>
        <pattern pattern="MINUS" color="#FF0000" isBold="true" />
      </patterns>
    </display>
    <display id="2" name="Red/Amber" state="REDAMBER">
      <patterns>
        <pattern pattern="FRAME" color="#CCCC00" isBold="true" />
        <pattern pattern="SLASH" color="#CC0000" isBold="false" />
        <pattern pattern="MINUS" color="#CC0000" isBold="false" />
      </patterns>
    </display>
    <display id="3" name="Green" state="GREEN">
      <patterns>
        <pattern pattern="FRAME" color="#00CC00" isBold="true" />
        <pattern pattern="SOLID" color="#00CC00" isBold="false" />
      </patterns>
    </display>
    <display id="4" name="Amber" state="AMBER">
      <patterns>
        <pattern pattern="FRAME" color="#CCCC00" isBold="true" />
        <pattern pattern="SLASH" color="#CCCC00" isBold="false" />
      </patterns>
    </display>
  </signaldisplays>
  <signalsequences>
    <signalsequence id="3" name="Red-Red/Amber-Green-Amber">
      <state display="1" isFixedDuration="false" isClosed="true" defaultDuration="1000" />
      <state display="2" isFixedDuration="true" isClosed="true" defaultDuration="1000" />
      <state display="3" isFixedDuration="false" isClosed="false" defaultDuration="5000" />
      <state display="4" isFixedDuration="true" isClosed="true" defaultDuration="3000" />
    </signalsequence>
    <signalsequence id="4" name="Red-Green">
      <state display="1" isFixedDuration="false" isClosed="true" defaultDuration="1000" />
      <state display="3" isFixedDuration="false" isClosed="false" defaultDuration="5000" />
    </signalsequence>
  </signalsequences>
  <sgs>
    <sg id="1" name="SG1" defaultSignalSequence="3" underEPICSControl="true">
      <defaultDurations>
        <defaultDuration display="1" duration="1000" />
        <defaultDuration display="2" duration="1000" />
        <defaultDuration display="3" duration="5000" />
        <defaultDuration display="4" duration="3000" />
      </defaultDurations>
      <EPICSTrafficDemands>
        <EPICSITDemand numberLanes="1" maximumSpeed="30" weight="1" timeRequirement="2000" helpSignalGroup="0" competingSignalGroup="0" useFlowProfiles="false" active="true">
          <occupancyDetectors />
          <subtractionDetectors />
          <ITDetectionPoints>
            <ITDetectionPoint travelTime="6000">
              <countingDetectors>
                <countingDetector countingDetId="5" />
              </countingDetectors>
            </ITDetectionPoint>
          </ITDetectionPoints>
        </EPICSITDemand>
        <EPICSPTDemand maximumSpeed="30" weight0="100" weight="100" weight2="100" weight3="100" timeRequirement="4000" helpSignalGroup="0" competingSignalGroup="0" active="true">
          <PTDetectionPoints>
            <PTDetectionPoint travelTime="30000" callingPointPair="1" hasOwnLane="false" fastestTravelTime="26000" slowTravelTime="38000" slowestTravelTime="42000" />
          </PTDetectionPoints>
        </EPICSPTDemand>
      </EPICSTrafficDemands>
    </sg>
    <sg id="2" name="SG2" defaultSignalSequence="3" underEPICSControl="true">
      <defaultDurations>
        <defaultDuration display="1" duration="1000" />
        <defaultDuration display="2" duration="1000" />
        <defaultDuration display="3" duration="5000" />
        <defaultDuration display="4" duration="3000" />
      </defaultDurations>
      <EPICSTrafficDemands>
        <EPICSITDemand numberLanes="1" maximumSpeed="40" weight="1" timeRequirement="2000" helpSignalGroup="0" competingSignalGroup="0" useFlowProfiles="false" active="true">
          <occupancyDetectors />
          <subtractionDetectors />
          <ITDetectionPoints>
            <ITDetectionPoint travelTime="5000">
              <countingDetectors>
                <countingDetector countingDetId="6" />
              </countingDetectors>
            </ITDetectionPoint>
          </ITDetectionPoints>
        </EPICSITDemand>
      </EPICSTrafficDemands>
    </sg>
    <sg id="3" name="SG3" defaultSignalSequence="3" underEPICSControl="true">
      <defaultDurations>
        <defaultDuration display="1" duration="1000" />
        <defaultDuration display="2" duration="1000" />
        <defaultDuration display="3" duration="5000" />
        <defaultDuration display="4" duration="3000" />
      </defaultDurations>
      <EPICSTrafficDemands>
        <EPICSITDemand numberLanes="1" maximumSpeed="30" weight="1" timeRequirement="2000" helpSignalGroup="0" competingSignalGroup="0" useFlowProfiles="false" active="true">
          <occupancyDetectors />
          <subtractionDetectors />
          <ITDetectionPoints>
            <ITDetectionPoint travelTime="6000">
              <countingDetectors>
                <countingDetector countingDetId="7" />
              </countingDetectors>
            </ITDetectionPoint>
          </ITDetectionPoints>
        </EPICSITDemand>
      </EPICSTrafficDemands>
    </sg>
    <sg id="4" name="SG4" defaultSignalSequence="3" underEPICSControl="true">
      <defaultDurations>
        <defaultDuration display="1" duration="1000" />
        <defaultDuration display="2" duration="1000" />
        <defaultDuration display="3" duration="5000" />
        <defaultDuration display="4" duration="3000" />
      </defaultDurations>
      <EPICSTrafficDemands>
        <EPICSITDemand numberLanes="1" maximumSpeed="40" weight="1" timeRequirement="2000" helpSignalGroup="0" competingSignalGroup="0" useFlowProfiles="false" active="true">
          <occupancyDetectors />
          <subtractionDetectors />
          <ITDetectionPoints>
            <ITDetectionPoint travelTime="5000">
              <countingDetectors>
                <countingDetector countingDetId="8" />
              </countingDetectors>
            </ITDetectionPoint>
          </ITDetectionPoints>
        </EPICSITDemand>
      </EPICSTrafficDemands>
    </sg>
    <sg id="5" name="Crosswalk1" defaultSignalSequence="4" underEPICSControl="true">
      <defaultDurations>
        <defaultDuration display="1" duration="1000" />
        <defaultDuration display="3" duration="5000" />
      </defaultDurations>
    </sg>
    <sg id="6" name="Crosswalk2" defaultSignalSequence="4" underEPICSControl="true">
      <defaultDurations>
        <defaultDuration display="1" duration="1000" />
        <defaultDuration display="3" duration="5000" />
      </defaultDurations>
    </sg>
    <sg id="7" name="Crosswalk3" defaultSignalSequence="4" underEPICSControl="true">
      <defaultDurations>
        <defaultDuration display="1" duration="1000" />
        <defaultDuration display="3" duration="5000" />
      </defaultDurations>
    </sg>
    <sg id="8" name="Crosswalk4" defaultSignalSequence="4" underEPICSControl="true">
      <defaultDurations>
        <defaultDuration display="1" duration="1000" />
        <defaultDuration display="3" duration="5000" />
      </defaultDurations>
    </sg>
  </sgs>
  <dets>
    <det id="1" name="13_Crosswalk_1" />
    <det id="2" name="13_Crosswalk_2" />
    <det id="3" name="13_Crosswalk_3" />
    <det id="4" name="13_Crosswalk_4" />
    <det id="5" name="13_SG_1_Lane1" />
    <det id="6" name="13_SG_2_Lane2" />
    <det id="7" name="13_SG_3_Lane2" />
    <det id="8" name="13_SG_4_Lane2" />
    <det id="9" name="13_SG_1_BusLogOn_Lane1" />
    <det id="10" name="13_SG_1_BusLogOff_Lane1" />
  </dets>
  <callingPointPairs>
    <callingPointPair id="1" name="East-West" vehicleTimeForcedLogOff="120000" signalGroupTimeForcedLogOff="0">
      <loginPoints>
        <loginPoint loginDetectorId="9" />
      </loginPoints>
      <logoffPoints>
        <logoffPoint logoffDetectorId="10" />
      </logoffPoints>
    </callingPointPair>
  </callingPointPairs>
  <intergreenmatrices>
    <intergreenmatrix id="1" name="IG_SC13">
      <intergreen clearingsg="4" enteringsg="1" value="2000" />
      <intergreen clearingsg="2" enteringsg="1" value="1000" />
      <intergreen clearingsg="5" enteringsg="1" value="4000" />
      <intergreen clearingsg="7" enteringsg="1" value="4000" />
      <intergreen clearingsg="1" enteringsg="2" value="2000" />
      <intergreen clearingsg="6" enteringsg="2" value="6000" />
      <intergreen clearingsg="8" enteringsg="2" value="4000" />
      <intergreen clearingsg="3" enteringsg="2" value="1000" />
      <intergreen clearingsg="2" enteringsg="3" value="2000" />
      <intergreen clearingsg="4" enteringsg="3" value="1000" />
      <intergreen clearingsg="7" enteringsg="3" value="6000" />
      <intergreen clearingsg="5" enteringsg="3" value="3000" />
      <intergreen clearingsg="1" enteringsg="4" value="2000" />
      <intergreen clearingsg="3" enteringsg="4" value="2000" />
      <intergreen clearingsg="6" enteringsg="4" value="4000" />
      <intergreen clearingsg="8" enteringsg="4" value="6000" />
      <intergreen clearingsg="1" enteringsg="5" value="1000" />
      <intergreen clearingsg="3" enteringsg="5" value="2000" />
      <intergreen clearingsg="2" enteringsg="6" value="1000" />
      <intergreen clearingsg="4" enteringsg="6" value="2000" />
      <intergreen clearingsg="1" enteringsg="7" value="2000" />
      <intergreen clearingsg="3" enteringsg="7" value="1000" />
      <intergreen clearingsg="2" enteringsg="8" value="2000" />
      <intergreen clearingsg="4" enteringsg="8" value="1000" />
    </intergreenmatrix>
  </intergreenmatrices>
  <progs />
  <stages>
    <stage id="1" name="Stage 1" isPseudoStage="false">
      <activations>
        <activation sg_id="1" activation="OFF" />
        <activation sg_id="2" activation="ON" />
        <activation sg_id="3" activation="OFF" />
        <activation sg_id="4" activation="ON" />
        <activation sg_id="5" activation="ON" />
        <activation sg_id="6" activation="OFF" />
        <activation sg_id="7" activation="ON" />
        <activation sg_id="8" activation="OFF" />
      </activations>
    </stage>
    <stage id="2" name="Stage 2" isPseudoStage="false">
      <activations>
        <activation sg_id="1" activation="ON" />
        <activation sg_id="2" activation="OFF" />
        <activation sg_id="3" activation="ON" />
        <activation sg_id="4" activation="OFF" />
        <activation sg_id="5" activation="OFF" />
        <activation sg_id="6" activation="ON" />
        <activation sg_id="7" activation="OFF" />
        <activation sg_id="8" activation="ON" />
      </activations>
    </stage>
  </stages>
  <interstageProgs>
    <interstageProg id="1" cycletime="6000" intergreens="1" fromStage="1" toStage="2" name="1: Stage 1->2: Stage 2" virtualDuration="6000">
      <sgs>
        <sg sg_id="1" signal_sequence="3">
          <cmds>
            <cmd display="1" begin="0" />
            <cmd display="3" begin="4000" />
          </cmds>
          <fixedstates>
            <fixedstate display="2" duration="1000" />
          </fixedstates>
        </sg>
        <sg sg_id="2" signal_sequence="3">
          <cmds>
            <cmd display="3" begin="0" />
            <cmd display="1" begin="3000" />
          </cmds>
          <fixedstates>
            <fixedstate display="4" duration="3000" />
          </fixedstates>
        </sg>
        <sg sg_id="3" signal_sequence="3">
          <cmds>
            <cmd display="1" begin="0" />
            <cmd display="3" begin="6000" />
          </cmds>
          <fixedstates>
            <fixedstate display="2" duration="1000" />
          </fixedstates>
        </sg>
        <sg sg_id="4" signal_sequence="3">
          <cmds>
            <cmd display="3" begin="0" />
            <cmd display="1" begin="3000" />
          </cmds>
          <fixedstates>
            <fixedstate display="4" duration="3000" />
          </fixedstates>
        </sg>
        <sg sg_id="5" signal_sequence="4">
          <cmds>
            <cmd display="3" begin="0" />
            <cmd display="1" begin="0" />
          </cmds>
          <fixedstates />
        </sg>
        <sg sg_id="6" signal_sequence="4">
          <cmds>
            <cmd display="1" begin="0" />
            <cmd display="3" begin="2000" />
          </cmds>
          <fixedstates />
        </sg>
        <sg sg_id="7" signal_sequence="4">
          <cmds>
            <cmd display="3" begin="0" />
            <cmd display="1" begin="0" />
          </cmds>
          <fixedstates />
        </sg>
        <sg sg_id="8" signal_sequence="4">
          <cmds>
            <cmd display="1" begin="0" />
            <cmd display="3" begin="2000" />
          </cmds>
          <fixedstates />
        </sg>
      </sgs>
    </interstageProg>
    <interstageProg id="2" cycletime="6000" intergreens="1" fromStage="2" toStage="1" name="2: Stage 2->1: Stage 1" virtualDuration="6000">
      <sgs>
        <sg sg_id="1" signal_sequence="3">
          <cmds>
            <cmd display="3" begin="0" />
            <cmd display="1" begin="3000" />
          </cmds>
          <fixedstates>
            <fixedstate display="4" duration="3000" />
          </fixedstates>
        </sg>
        <sg sg_id="2" signal_sequence="3">
          <cmds>
            <cmd display="1" begin="0" />
            <cmd display="3" begin="6000" />
          </cmds>
          <fixedstates>
            <fixedstate display="2" duration="1000" />
          </fixedstates>
        </sg>
        <sg sg_id="3" signal_sequence="3">
          <cmds>
            <cmd display="3" begin="0" />
            <cmd display="1" begin="3000" />
          </cmds>
          <fixedstates>
            <fixedstate display="4" duration="3000" />
          </fixedstates>
        </sg>
        <sg sg_id="4" signal_sequence="3">
          <cmds>
            <cmd display="1" begin="0" />
            <cmd display="3" begin="6000" />
          </cmds>
          <fixedstates>
            <fixedstate display="2" duration="1000" />
          </fixedstates>
        </sg>
        <sg sg_id="5" signal_sequence="4">
          <cmds>
            <cmd display="1" begin="0" />
            <cmd display="3" begin="2000" />
          </cmds>
          <fixedstates />
        </sg>
        <sg sg_id="6" signal_sequence="4">
          <cmds>
            <cmd display="3" begin="0" />
            <cmd display="1" begin="0" />
          </cmds>
          <fixedstates />
        </sg>
        <sg sg_id="7" signal_sequence="4">
          <cmds>
            <cmd display="1" begin="0" />
            <cmd display="3" begin="2000" />
          </cmds>
          <fixedstates />
        </sg>
        <sg sg_id="8" signal_sequence="4">
          <cmds>
            <cmd display="3" begin="0" />
            <cmd display="1" begin="0" />
          </cmds>
          <fixedstates />
        </sg>
      </sgs>
    </interstageProg>
  </interstageProgs>
  <stageProgs>
    <stageProg id="1" cycletime="90000" switchpoint="0" offset="29000" intergreens="1" fitness="0.000000" vehicleCount="0" weightBalance="3" weightStops="0" balanceFixedTimeControl="false" name="Stage 1, Stage 2">
      <interstages>
        <interstage display="1" begin="0" />
        <interstage display="2" begin="41000" />
      </interstages>
      <BALANCEInterstages>
        <BALANCEInterstage balIstId="1" earliestStart="0" originalStart="0" latestStart="89000" notes="" />
        <BALANCEInterstage balIstId="2" earliestStart="0" originalStart="41000" latestStart="89000" notes="" />
      </BALANCEInterstages>
      <activeInterstages>
        <activeInterstage actIstId="1" />
        <activeInterstage actIstId="2" />
      </activeInterstages>
      <EPICSStageParameters>
        <EPICSStageParameter stageId="1" earliestStart="0" latestEnd="90000" minimumLength="0" maximumLength="125000" preferredStart="47000" preferredEnd="0" costPreferred="0" costNonPreferred="5" notes="" />
        <EPICSStageParameter stageId="2" earliestStart="0" latestEnd="90000" minimumLength="0" maximumLength="125000" preferredStart="6000" preferredEnd="41000" costPreferred="0" costNonPreferred="5" notes="" />
      </EPICSStageParameters>
      <sgs>
        <sg sg_id="1" cyclical="true" epicsMinRed="0" epicsMaxRed="90000" balMinGreen="5000" balMaxGreen="90000" balWeightDelay="1.000000" balWeightQueue="10.000000" balWeightStops="50.000000" notes="" />
        <sg sg_id="2" cyclical="true" epicsMinRed="0" epicsMaxRed="90000" balMinGreen="5000" balMaxGreen="90000" balWeightDelay="1.000000" balWeightQueue="10.000000" balWeightStops="50.000000" notes="" />
        <sg sg_id="3" cyclical="true" epicsMinRed="0" epicsMaxRed="90000" balMinGreen="5000" balMaxGreen="90000" balWeightDelay="1.000000" balWeightQueue="10.000000" balWeightStops="50.000000" notes="" />
        <sg sg_id="4" cyclical="true" epicsMinRed="0" epicsMaxRed="90000" balMinGreen="5000" balMaxGreen="90000" balWeightDelay="1.000000" balWeightQueue="10.000000" balWeightStops="50.000000" notes="" />
        <sg sg_id="5" cyclical="true" epicsMinRed="0" epicsMaxRed="90000" balMinGreen="5000" balMaxGreen="90000" balWeightDelay="1.000000" balWeightQueue="10.000000" balWeightStops="50.000000" notes="" />
        <sg sg_id="6" cyclical="true" epicsMinRed="0" epicsMaxRed="90000" balMinGreen="5000" balMaxGreen="90000" balWeightDelay="1.000000" balWeightQueue="10.000000" balWeightStops="50.000000" notes="" />
        <sg sg_id="7" cyclical="true" epicsMinRed="0" epicsMaxRed="90000" balMinGreen="5000" balMaxGreen="90000" balWeightDelay="1.000000" balWeightQueue="10.000000" balWeightStops="50.000000" notes="" />
        <sg sg_id="8" cyclical="true" epicsMinRed="0" epicsMaxRed="90000" balMinGreen="5000" balMaxGreen="90000" balWeightDelay="1.000000" balWeightQueue="10.000000" balWeightStops="50.000000" notes="" />
      </sgs>
    </stageProg>
    <stageProg id="2" cycletime="90000" switchpoint="0" offset="29000" intergreens="1" fitness="0.000000" vehicleCount="0" weightBalance="1" weightStops="0" balanceFixedTimeControl="true" name="Stage 1, Stage 2">
      <interstages>
        <interstage display="1" begin="0" />
        <interstage display="2" begin="41000" />
      </interstages>
      <BALANCEInterstages>
        <BALANCEInterstage balIstId="1" earliestStart="0" originalStart="0" latestStart="89000" notes="" />
        <BALANCEInterstage balIstId="2" earliestStart="0" originalStart="41000" latestStart="89000" notes="" />
      </BALANCEInterstages>
      <activeInterstages>
        <activeInterstage actIstId="1" />
        <activeInterstage actIstId="2" />
      </activeInterstages>
      <EPICSStageParameters>
        <EPICSStageParameter stageId="1" earliestStart="0" latestEnd="90000" minimumLength="0" maximumLength="125000" preferredStart="47000" preferredEnd="0" costPreferred="0" costNonPreferred="5" notes="" />
        <EPICSStageParameter stageId="2" earliestStart="0" latestEnd="90000" minimumLength="0" maximumLength="125000" preferredStart="6000" preferredEnd="41000" costPreferred="0" costNonPreferred="5" notes="" />
      </EPICSStageParameters>
      <sgs>
        <sg sg_id="1" cyclical="true" epicsMinRed="0" epicsMaxRed="90000" balMinGreen="5000" balMaxGreen="90000" balWeightDelay="1.000000" balWeightQueue="10.000000" balWeightStops="50.000000" notes="" />
        <sg sg_id="2" cyclical="true" epicsMinRed="0" epicsMaxRed="90000" balMinGreen="5000" balMaxGreen="90000" balWeightDelay="1.000000" balWeightQueue="10.000000" balWeightStops="50.000000" notes="" />
        <sg sg_id="3" cyclical="true" epicsMinRed="0" epicsMaxRed="90000" balMinGreen="5000" balMaxGreen="90000" balWeightDelay="1.000000" balWeightQueue="10.000000" balWeightStops="50.000000" notes="" />
        <sg sg_id="4" cyclical="true" epicsMinRed="0" epicsMaxRed="90000" balMinGreen="5000" balMaxGreen="90000" balWeightDelay="1.000000" balWeightQueue="10.000000" balWeightStops="50.000000" notes="" />
        <sg sg_id="5" cyclical="true" epicsMinRed="0" epicsMaxRed="90000" balMinGreen="5000" balMaxGreen="90000" balWeightDelay="1.000000" balWeightQueue="10.000000" balWeightStops="50.000000" notes="" />
        <sg sg_id="6" cyclical="true" epicsMinRed="0" epicsMaxRed="90000" balMinGreen="5000" balMaxGreen="90000" balWeightDelay="1.000000" balWeightQueue="10.000000" balWeightStops="50.000000" notes="" />
        <sg sg_id="7" cyclical="true" epicsMinRed="0" epicsMaxRed="90000" balMinGreen="5000" balMaxGreen="90000" balWeightDelay="1.000000" balWeightQueue="10.000000" balWeightStops="50.000000" notes="" />
        <sg sg_id="8" cyclical="true" epicsMinRed="0" epicsMaxRed="90000" balMinGreen="5000" balMaxGreen="90000" balWeightDelay="1.000000" balWeightQueue="10.000000" balWeightStops="50.000000" notes="" />
      </sgs>
    </stageProg>
  </stageProgs>
  <dailyProgLists />
</sc>