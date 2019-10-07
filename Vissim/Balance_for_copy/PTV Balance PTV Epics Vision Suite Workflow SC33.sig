<?xml version="1.0" encoding="UTF-8"?>
<sc version="201602" id="33" name="SC33" frequency="1" steps="0" defaultIntergreenMatrix="1" EPICSTimeHorizon="100000" EPICSLogLevel="1" interstagesUsingMinDurations="false" checkSum="1848499048">
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
        <EPICSITDemand numberLanes="2" maximumSpeed="50" weight="1" timeRequirement="2000" helpSignalGroup="0" competingSignalGroup="0" useFlowProfiles="false" active="true">
          <occupancyDetectors />
          <subtractionDetectors />
          <ITDetectionPoints>
            <ITDetectionPoint travelTime="4000">
              <countingDetectors>
                <countingDetector countingDetId="6" />
                <countingDetector countingDetId="10" />
              </countingDetectors>
            </ITDetectionPoint>
          </ITDetectionPoints>
        </EPICSITDemand>
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
        <EPICSITDemand numberLanes="1" maximumSpeed="40" weight="2" timeRequirement="2000" helpSignalGroup="0" competingSignalGroup="0" useFlowProfiles="false" active="true">
          <occupancyDetectors />
          <subtractionDetectors />
          <ITDetectionPoints>
            <ITDetectionPoint travelTime="5000">
              <countingDetectors>
                <countingDetector countingDetId="7" />
              </countingDetectors>
            </ITDetectionPoint>
          </ITDetectionPoints>
        </EPICSITDemand>
      </EPICSTrafficDemands>
    </sg>
    <sg id="3" name="SG3L" defaultSignalSequence="3" underEPICSControl="true">
      <defaultDurations>
        <defaultDuration display="1" duration="1000" />
        <defaultDuration display="2" duration="1000" />
        <defaultDuration display="3" duration="5000" />
        <defaultDuration display="4" duration="3000" />
      </defaultDurations>
      <EPICSTrafficDemands>
        <EPICSITDemand numberLanes="1" maximumSpeed="50" weight="1" timeRequirement="2000" helpSignalGroup="0" competingSignalGroup="0" useFlowProfiles="false" active="true">
          <occupancyDetectors />
          <subtractionDetectors />
          <ITDetectionPoints>
            <ITDetectionPoint travelTime="1000">
              <countingDetectors>
                <countingDetector countingDetId="9" />
              </countingDetectors>
            </ITDetectionPoint>
          </ITDetectionPoints>
        </EPICSITDemand>
      </EPICSTrafficDemands>
    </sg>
    <sg id="4" name="SG3SR" defaultSignalSequence="3" underEPICSControl="true">
      <defaultDurations>
        <defaultDuration display="1" duration="1000" />
        <defaultDuration display="2" duration="1000" />
        <defaultDuration display="3" duration="5000" />
        <defaultDuration display="4" duration="3000" />
      </defaultDurations>
      <EPICSTrafficDemands>
        <EPICSITDemand numberLanes="2" maximumSpeed="50" weight="1" timeRequirement="2000" helpSignalGroup="0" competingSignalGroup="0" useFlowProfiles="false" active="true">
          <occupancyDetectors />
          <subtractionDetectors />
          <ITDetectionPoints>
            <ITDetectionPoint travelTime="1000">
              <countingDetectors>
                <countingDetector countingDetId="8" />
                <countingDetector countingDetId="11" />
              </countingDetectors>
            </ITDetectionPoint>
          </ITDetectionPoints>
        </EPICSITDemand>
      </EPICSTrafficDemands>
    </sg>
    <sg id="5" name="Crosswalk1S" defaultSignalSequence="4" underEPICSControl="true">
      <defaultDurations>
        <defaultDuration display="1" duration="1000" />
        <defaultDuration display="3" duration="5000" />
      </defaultDurations>
    </sg>
    <sg id="6" name="Crosswalk1N" defaultSignalSequence="4" underEPICSControl="true">
      <defaultDurations>
        <defaultDuration display="1" duration="1000" />
        <defaultDuration display="3" duration="5000" />
      </defaultDurations>
    </sg>
    <sg id="7" name="Crosswalk2" defaultSignalSequence="4" underEPICSControl="true">
      <defaultDurations>
        <defaultDuration display="1" duration="1000" />
        <defaultDuration display="3" duration="5000" />
      </defaultDurations>
    </sg>
    <sg id="8" name="Crosswalk3N" defaultSignalSequence="4" underEPICSControl="true">
      <defaultDurations>
        <defaultDuration display="1" duration="1000" />
        <defaultDuration display="3" duration="5000" />
      </defaultDurations>
    </sg>
    <sg id="9" name="Crosswalk3S" defaultSignalSequence="4" underEPICSControl="true">
      <defaultDurations>
        <defaultDuration display="1" duration="1000" />
        <defaultDuration display="3" duration="5000" />
      </defaultDurations>
    </sg>
  </sgs>
  <dets>
    <det id="1" name="33_Crosswalk_1N" />
    <det id="2" name="33_Crosswalk_1S" />
    <det id="3" name="33_Crosswalk_2" />
    <det id="4" name="33_Crosswalk_3N" />
    <det id="5" name="33_Crosswalk_3S" />
    <det id="6" name="33_SG_1_Lane3" />
    <det id="7" name="33_SG_2_Lane2" />
    <det id="8" name="33_SG_3_Lane4" />
    <det id="9" name="33_SG_3_Lane3" />
    <det id="10" name="33_SG_1_Lane4" />
    <det id="11" name="33_SG_3_Lane5" />
  </dets>
  <intergreenmatrices>
    <intergreenmatrix id="1" name="IG_SC33">
      <intergreen clearingsg="2" enteringsg="1" value="2000" />
      <intergreen clearingsg="3" enteringsg="1" value="3000" />
      <intergreen clearingsg="6" enteringsg="1" value="8000" />
      <intergreen clearingsg="8" enteringsg="1" value="5000" />
      <intergreen clearingsg="1" enteringsg="2" value="3000" />
      <intergreen clearingsg="3" enteringsg="2" value="2000" />
      <intergreen clearingsg="4" enteringsg="2" value="3000" />
      <intergreen clearingsg="7" enteringsg="2" value="6000" />
      <intergreen clearingsg="1" enteringsg="3" value="3000" />
      <intergreen clearingsg="2" enteringsg="3" value="3000" />
      <intergreen clearingsg="7" enteringsg="3" value="6000" />
      <intergreen clearingsg="9" enteringsg="3" value="9000" />
      <intergreen clearingsg="2" enteringsg="4" value="3000" />
      <intergreen clearingsg="5" enteringsg="4" value="5000" />
      <intergreen clearingsg="9" enteringsg="4" value="9000" />
      <intergreen clearingsg="4" enteringsg="5" value="4000" />
      <intergreen clearingsg="1" enteringsg="6" value="2000" />
      <intergreen clearingsg="2" enteringsg="7" value="2000" />
      <intergreen clearingsg="3" enteringsg="7" value="3000" />
      <intergreen clearingsg="1" enteringsg="8" value="3000" />
      <intergreen clearingsg="3" enteringsg="9" value="2000" />
      <intergreen clearingsg="4" enteringsg="9" value="2000" />
    </intergreenmatrix>
  </intergreenmatrices>
  <progs />
  <stages>
    <stage id="1" name="Stage 1" isPseudoStage="false">
      <activations>
        <activation sg_id="1" activation="ON" />
        <activation sg_id="2" activation="OFF" />
        <activation sg_id="3" activation="OFF" />
        <activation sg_id="4" activation="ON" />
        <activation sg_id="5" activation="OFF" />
        <activation sg_id="6" activation="OFF" />
        <activation sg_id="7" activation="ON" />
        <activation sg_id="8" activation="OFF" />
        <activation sg_id="9" activation="OFF" />
      </activations>
    </stage>
    <stage id="2" name="Stage 2" isPseudoStage="false">
      <activations>
        <activation sg_id="1" activation="OFF" />
        <activation sg_id="2" activation="OFF" />
        <activation sg_id="3" activation="ON" />
        <activation sg_id="4" activation="ON" />
        <activation sg_id="5" activation="OFF" />
        <activation sg_id="6" activation="OFF" />
        <activation sg_id="7" activation="OFF" />
        <activation sg_id="8" activation="OFF" />
        <activation sg_id="9" activation="OFF" />
      </activations>
    </stage>
    <stage id="3" name="Stage 3" isPseudoStage="false">
      <activations>
        <activation sg_id="1" activation="OFF" />
        <activation sg_id="2" activation="ON" />
        <activation sg_id="3" activation="OFF" />
        <activation sg_id="4" activation="OFF" />
        <activation sg_id="5" activation="ON" />
        <activation sg_id="6" activation="ON" />
        <activation sg_id="7" activation="OFF" />
        <activation sg_id="8" activation="ON" />
        <activation sg_id="9" activation="ON" />
      </activations>
    </stage>
  </stages>
  <interstageProgs>
    <interstageProg id="1" cycletime="6000" intergreens="1" fromStage="1" toStage="2" name="1: Stage 1->2: Stage 2" virtualDuration="6000">
      <sgs>
        <sg sg_id="1" signal_sequence="3">
          <cmds>
            <cmd display="3" begin="0" />
            <cmd display="1" begin="6000" />
          </cmds>
          <fixedstates>
            <fixedstate display="4" duration="3000" />
          </fixedstates>
        </sg>
        <sg sg_id="2" signal_sequence="1">
          <cmds />
          <fixedstates />
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
        <sg sg_id="4" signal_sequence="2">
          <cmds />
          <fixedstates />
        </sg>
        <sg sg_id="5" signal_sequence="1">
          <cmds />
          <fixedstates />
        </sg>
        <sg sg_id="6" signal_sequence="1">
          <cmds />
          <fixedstates />
        </sg>
        <sg sg_id="7" signal_sequence="4">
          <cmds>
            <cmd display="3" begin="0" />
            <cmd display="1" begin="0" />
          </cmds>
          <fixedstates />
        </sg>
        <sg sg_id="8" signal_sequence="1">
          <cmds />
          <fixedstates />
        </sg>
        <sg sg_id="9" signal_sequence="1">
          <cmds />
          <fixedstates />
        </sg>
      </sgs>
    </interstageProg>
    <interstageProg id="2" cycletime="6000" intergreens="1" fromStage="1" toStage="3" name="1: Stage 1->3: Stage 3" virtualDuration="6000">
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
        <sg sg_id="3" signal_sequence="1">
          <cmds />
          <fixedstates />
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
            <cmd display="1" begin="0" />
            <cmd display="3" begin="4000" />
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
            <cmd display="3" begin="3000" />
          </cmds>
          <fixedstates />
        </sg>
        <sg sg_id="9" signal_sequence="4">
          <cmds>
            <cmd display="1" begin="0" />
            <cmd display="3" begin="2000" />
          </cmds>
          <fixedstates />
        </sg>
      </sgs>
    </interstageProg>
    <interstageProg id="3" cycletime="3000" intergreens="1" fromStage="2" toStage="1" name="2: Stage 2->1: Stage 1" virtualDuration="3000">
      <sgs>
        <sg sg_id="1" signal_sequence="3">
          <cmds>
            <cmd display="1" begin="0" />
            <cmd display="3" begin="3000" />
          </cmds>
          <fixedstates>
            <fixedstate display="2" duration="1000" />
          </fixedstates>
        </sg>
        <sg sg_id="2" signal_sequence="1">
          <cmds />
          <fixedstates />
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
        <sg sg_id="4" signal_sequence="2">
          <cmds />
          <fixedstates />
        </sg>
        <sg sg_id="5" signal_sequence="1">
          <cmds />
          <fixedstates />
        </sg>
        <sg sg_id="6" signal_sequence="1">
          <cmds />
          <fixedstates />
        </sg>
        <sg sg_id="7" signal_sequence="4">
          <cmds>
            <cmd display="1" begin="0" />
            <cmd display="3" begin="3000" />
          </cmds>
          <fixedstates />
        </sg>
        <sg sg_id="8" signal_sequence="1">
          <cmds />
          <fixedstates />
        </sg>
        <sg sg_id="9" signal_sequence="1">
          <cmds />
          <fixedstates />
        </sg>
      </sgs>
    </interstageProg>
    <interstageProg id="4" cycletime="4000" intergreens="1" fromStage="2" toStage="3" name="2: Stage 2->3: Stage 3" virtualDuration="4000">
      <sgs>
        <sg sg_id="1" signal_sequence="1">
          <cmds />
          <fixedstates />
        </sg>
        <sg sg_id="2" signal_sequence="3">
          <cmds>
            <cmd display="1" begin="0" />
            <cmd display="3" begin="3000" />
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
            <cmd display="3" begin="0" />
            <cmd display="1" begin="3000" />
          </cmds>
          <fixedstates>
            <fixedstate display="4" duration="3000" />
          </fixedstates>
        </sg>
        <sg sg_id="5" signal_sequence="4">
          <cmds>
            <cmd display="1" begin="0" />
            <cmd display="3" begin="4000" />
          </cmds>
          <fixedstates />
        </sg>
        <sg sg_id="6" signal_sequence="4">
          <cmds>
            <cmd display="1" begin="0" />
            <cmd display="3" begin="0" />
          </cmds>
          <fixedstates />
        </sg>
        <sg sg_id="7" signal_sequence="1">
          <cmds />
          <fixedstates />
        </sg>
        <sg sg_id="8" signal_sequence="4">
          <cmds>
            <cmd display="1" begin="0" />
            <cmd display="3" begin="0" />
          </cmds>
          <fixedstates />
        </sg>
        <sg sg_id="9" signal_sequence="4">
          <cmds>
            <cmd display="1" begin="0" />
            <cmd display="3" begin="2000" />
          </cmds>
          <fixedstates />
        </sg>
      </sgs>
    </interstageProg>
    <interstageProg id="5" cycletime="9000" intergreens="1" fromStage="3" toStage="1" name="3: Stage 3->1: Stage 1" virtualDuration="9000">
      <sgs>
        <sg sg_id="1" signal_sequence="3">
          <cmds>
            <cmd display="1" begin="0" />
            <cmd display="3" begin="8000" />
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
        <sg sg_id="3" signal_sequence="1">
          <cmds />
          <fixedstates />
        </sg>
        <sg sg_id="4" signal_sequence="3">
          <cmds>
            <cmd display="1" begin="0" />
            <cmd display="3" begin="9000" />
          </cmds>
          <fixedstates>
            <fixedstate display="2" duration="1000" />
          </fixedstates>
        </sg>
        <sg sg_id="5" signal_sequence="4">
          <cmds>
            <cmd display="3" begin="0" />
            <cmd display="1" begin="4000" />
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
            <cmd display="1" begin="3000" />
          </cmds>
          <fixedstates />
        </sg>
        <sg sg_id="9" signal_sequence="4">
          <cmds>
            <cmd display="3" begin="0" />
            <cmd display="1" begin="0" />
          </cmds>
          <fixedstates />
        </sg>
      </sgs>
    </interstageProg>
    <interstageProg id="6" cycletime="9000" intergreens="1" fromStage="3" toStage="2" name="3: Stage 3->2: Stage 2" virtualDuration="9000">
      <sgs>
        <sg sg_id="1" signal_sequence="1">
          <cmds />
          <fixedstates />
        </sg>
        <sg sg_id="2" signal_sequence="3">
          <cmds>
            <cmd display="3" begin="0" />
            <cmd display="1" begin="9000" />
          </cmds>
          <fixedstates>
            <fixedstate display="4" duration="3000" />
          </fixedstates>
        </sg>
        <sg sg_id="3" signal_sequence="3">
          <cmds>
            <cmd display="1" begin="0" />
            <cmd display="3" begin="9000" />
          </cmds>
          <fixedstates>
            <fixedstate display="2" duration="1000" />
          </fixedstates>
        </sg>
        <sg sg_id="4" signal_sequence="3">
          <cmds>
            <cmd display="1" begin="0" />
            <cmd display="3" begin="9000" />
          </cmds>
          <fixedstates>
            <fixedstate display="2" duration="1000" />
          </fixedstates>
        </sg>
        <sg sg_id="5" signal_sequence="4">
          <cmds>
            <cmd display="3" begin="0" />
            <cmd display="1" begin="4000" />
          </cmds>
          <fixedstates />
        </sg>
        <sg sg_id="6" signal_sequence="4">
          <cmds>
            <cmd display="3" begin="0" />
            <cmd display="1" begin="9000" />
          </cmds>
          <fixedstates />
        </sg>
        <sg sg_id="7" signal_sequence="1">
          <cmds />
          <fixedstates />
        </sg>
        <sg sg_id="8" signal_sequence="4">
          <cmds>
            <cmd display="3" begin="0" />
            <cmd display="1" begin="9000" />
          </cmds>
          <fixedstates />
        </sg>
        <sg sg_id="9" signal_sequence="4">
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
    <stageProg id="1" cycletime="90000" switchpoint="0" offset="86000" intergreens="1" fitness="0.000000" vehicleCount="0" weightBalance="5" weightStops="0" balanceFixedTimeControl="false" name="Stage 1, Stage 2, Stage 3">
      <interstages>
        <interstage display="1" begin="0" />
        <interstage display="4" begin="12000" />
        <interstage display="5" begin="41000" />
      </interstages>
      <BALANCEInterstages>
        <BALANCEInterstage balIstId="1" earliestStart="0" originalStart="0" latestStart="89000" notes="" />
        <BALANCEInterstage balIstId="4" earliestStart="0" originalStart="12000" latestStart="89000" notes="" />
        <BALANCEInterstage balIstId="5" earliestStart="0" originalStart="41000" latestStart="89000" notes="" />
      </BALANCEInterstages>
      <activeInterstages>
        <activeInterstage actIstId="1" />
        <activeInterstage actIstId="4" />
        <activeInterstage actIstId="5" />
      </activeInterstages>
      <EPICSStageParameters>
        <EPICSStageParameter stageId="1" earliestStart="0" latestEnd="90000" minimumLength="0" maximumLength="125000" preferredStart="50000" preferredEnd="0" costPreferred="0" costNonPreferred="20" notes="" />
        <EPICSStageParameter stageId="2" earliestStart="0" latestEnd="90000" minimumLength="0" maximumLength="125000" preferredStart="6000" preferredEnd="12000" costPreferred="0" costNonPreferred="20" notes="" />
        <EPICSStageParameter stageId="3" earliestStart="0" latestEnd="90000" minimumLength="0" maximumLength="125000" preferredStart="16000" preferredEnd="41000" costPreferred="0" costNonPreferred="20" notes="" />
      </EPICSStageParameters>
      <sgs>
        <sg sg_id="1" cyclical="true" epicsMinRed="0" epicsMaxRed="90000" balMinGreen="5000" balMaxGreen="90000" balWeightDelay="1.000000" balWeightQueue="10.000000" balWeightStops="50.000000" notes="" />
        <sg sg_id="2" cyclical="true" epicsMinRed="0" epicsMaxRed="90000" balMinGreen="5000" balMaxGreen="90000" balWeightDelay="1.000000" balWeightQueue="10.000000" balWeightStops="50.000000" notes="" />
        <sg sg_id="3" cyclical="true" epicsMinRed="0" epicsMaxRed="90000" balMinGreen="5000" balMaxGreen="90000" balWeightDelay="1.000000" balWeightQueue="10.000000" balWeightStops="50.000000" notes="" />
        <sg sg_id="4" cyclical="true" epicsMinRed="0" epicsMaxRed="90000" balMinGreen="6000" balMaxGreen="90000" balWeightDelay="1.000000" balWeightQueue="10.000000" balWeightStops="50.000000" notes="" />
        <sg sg_id="5" cyclical="true" epicsMinRed="0" epicsMaxRed="90000" balMinGreen="5000" balMaxGreen="90000" balWeightDelay="1.000000" balWeightQueue="10.000000" balWeightStops="50.000000" notes="" />
        <sg sg_id="6" cyclical="true" epicsMinRed="0" epicsMaxRed="90000" balMinGreen="5000" balMaxGreen="90000" balWeightDelay="1.000000" balWeightQueue="10.000000" balWeightStops="50.000000" notes="" />
        <sg sg_id="7" cyclical="true" epicsMinRed="0" epicsMaxRed="90000" balMinGreen="7000" balMaxGreen="90000" balWeightDelay="1.000000" balWeightQueue="10.000000" balWeightStops="50.000000" notes="" />
        <sg sg_id="8" cyclical="true" epicsMinRed="0" epicsMaxRed="90000" balMinGreen="7000" balMaxGreen="90000" balWeightDelay="1.000000" balWeightQueue="10.000000" balWeightStops="50.000000" notes="" />
        <sg sg_id="9" cyclical="true" epicsMinRed="0" epicsMaxRed="90000" balMinGreen="5000" balMaxGreen="90000" balWeightDelay="1.000000" balWeightQueue="10.000000" balWeightStops="50.000000" notes="" />
      </sgs>
    </stageProg>
    <stageProg id="2" cycletime="90000" switchpoint="0" offset="86000" intergreens="1" fitness="0.000000" vehicleCount="0" weightBalance="1" weightStops="0" balanceFixedTimeControl="true" name="Stage 1, Stage 2, Stage 3">
      <interstages>
        <interstage display="1" begin="0" />
        <interstage display="4" begin="12000" />
        <interstage display="5" begin="41000" />
      </interstages>
      <BALANCEInterstages>
        <BALANCEInterstage balIstId="1" earliestStart="0" originalStart="0" latestStart="89000" notes="" />
        <BALANCEInterstage balIstId="4" earliestStart="0" originalStart="12000" latestStart="89000" notes="" />
        <BALANCEInterstage balIstId="5" earliestStart="0" originalStart="41000" latestStart="89000" notes="" />
      </BALANCEInterstages>
      <activeInterstages>
        <activeInterstage actIstId="1" />
        <activeInterstage actIstId="4" />
        <activeInterstage actIstId="5" />
      </activeInterstages>
      <EPICSStageParameters>
        <EPICSStageParameter stageId="1" earliestStart="0" latestEnd="90000" minimumLength="0" maximumLength="125000" preferredStart="50000" preferredEnd="0" costPreferred="0" costNonPreferred="5" notes="" />
        <EPICSStageParameter stageId="2" earliestStart="0" latestEnd="90000" minimumLength="0" maximumLength="125000" preferredStart="6000" preferredEnd="12000" costPreferred="0" costNonPreferred="5" notes="" />
        <EPICSStageParameter stageId="3" earliestStart="0" latestEnd="90000" minimumLength="0" maximumLength="125000" preferredStart="16000" preferredEnd="41000" costPreferred="0" costNonPreferred="5" notes="" />
      </EPICSStageParameters>
      <sgs>
        <sg sg_id="1" cyclical="true" epicsMinRed="0" epicsMaxRed="90000" balMinGreen="5000" balMaxGreen="90000" balWeightDelay="1.000000" balWeightQueue="10.000000" balWeightStops="50.000000" notes="" />
        <sg sg_id="2" cyclical="true" epicsMinRed="0" epicsMaxRed="90000" balMinGreen="5000" balMaxGreen="90000" balWeightDelay="1.000000" balWeightQueue="10.000000" balWeightStops="50.000000" notes="" />
        <sg sg_id="3" cyclical="true" epicsMinRed="0" epicsMaxRed="90000" balMinGreen="5000" balMaxGreen="90000" balWeightDelay="1.000000" balWeightQueue="10.000000" balWeightStops="50.000000" notes="" />
        <sg sg_id="4" cyclical="true" epicsMinRed="0" epicsMaxRed="90000" balMinGreen="6000" balMaxGreen="90000" balWeightDelay="1.000000" balWeightQueue="10.000000" balWeightStops="50.000000" notes="" />
        <sg sg_id="5" cyclical="true" epicsMinRed="0" epicsMaxRed="90000" balMinGreen="5000" balMaxGreen="90000" balWeightDelay="1.000000" balWeightQueue="10.000000" balWeightStops="50.000000" notes="" />
        <sg sg_id="6" cyclical="true" epicsMinRed="0" epicsMaxRed="90000" balMinGreen="5000" balMaxGreen="90000" balWeightDelay="1.000000" balWeightQueue="10.000000" balWeightStops="50.000000" notes="" />
        <sg sg_id="7" cyclical="true" epicsMinRed="0" epicsMaxRed="90000" balMinGreen="7000" balMaxGreen="90000" balWeightDelay="1.000000" balWeightQueue="10.000000" balWeightStops="50.000000" notes="" />
        <sg sg_id="8" cyclical="true" epicsMinRed="0" epicsMaxRed="90000" balMinGreen="7000" balMaxGreen="90000" balWeightDelay="1.000000" balWeightQueue="10.000000" balWeightStops="50.000000" notes="" />
        <sg sg_id="9" cyclical="true" epicsMinRed="0" epicsMaxRed="90000" balMinGreen="5000" balMaxGreen="90000" balWeightDelay="1.000000" balWeightQueue="10.000000" balWeightStops="50.000000" notes="" />
      </sgs>
    </stageProg>
  </stageProgs>
  <dailyProgLists />
</sc>