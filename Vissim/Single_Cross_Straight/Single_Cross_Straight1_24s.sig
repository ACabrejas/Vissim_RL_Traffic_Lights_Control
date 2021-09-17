<?xml version="1.0" encoding="UTF-8"?>
<sc version="202001" id="3" name="" frequency="1" steps="0" defaultIntergreenMatrix="0" interstagesUsingMinDurations="true" checkSum="2087200078">
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
  </signalsequences>
  <sgs>
    <sg id="1" name="South" defaultSignalSequence="3">
      <defaultDurations>
        <defaultDuration display="1" duration="1000" />
        <defaultDuration display="2" duration="0" />
        <defaultDuration display="3" duration="5000" />
        <defaultDuration display="4" duration="3000" />
      </defaultDurations>
    </sg>
    <sg id="2" name="West" defaultSignalSequence="3">
      <defaultDurations>
        <defaultDuration display="1" duration="1000" />
        <defaultDuration display="2" duration="0" />
        <defaultDuration display="3" duration="5000" />
        <defaultDuration display="4" duration="3000" />
      </defaultDurations>
    </sg>
    <sg id="3" name="North" defaultSignalSequence="3">
      <defaultDurations>
        <defaultDuration display="1" duration="1000" />
        <defaultDuration display="2" duration="0" />
        <defaultDuration display="3" duration="5000" />
        <defaultDuration display="4" duration="3000" />
      </defaultDurations>
    </sg>
    <sg id="4" name="East" defaultSignalSequence="3">
      <defaultDurations>
        <defaultDuration display="1" duration="1000" />
        <defaultDuration display="2" duration="0" />
        <defaultDuration display="3" duration="5000" />
        <defaultDuration display="4" duration="3000" />
      </defaultDurations>
    </sg>
  </sgs>
  <intergreenmatrices>
    <intergreenmatrix id="1" name="Intergreen matrix 1">
      <intergreen clearingsg="1" enteringsg="2" value="3000" />
      <intergreen clearingsg="1" enteringsg="4" value="3000" />
      <intergreen clearingsg="3" enteringsg="2" value="3000" />
      <intergreen clearingsg="3" enteringsg="4" value="3000" />
      <intergreen clearingsg="4" enteringsg="1" value="3000" />
      <intergreen clearingsg="2" enteringsg="3" value="3000" />
      <intergreen clearingsg="4" enteringsg="3" value="3000" />
      <intergreen clearingsg="2" enteringsg="1" value="3000" />
      <intergreen clearingsg="1" enteringsg="3" value="3000" />
      <intergreen clearingsg="4" enteringsg="2" value="3000" />
      <intergreen clearingsg="3" enteringsg="1" value="3000" />
      <intergreen clearingsg="2" enteringsg="4" value="3000" />
    </intergreenmatrix>
  </intergreenmatrices>
  <progs>
    <prog id="1" cycletime="52000" switchpoint="0" offset="0" intergreens="0" fitness="0.000000" vehicleCount="0" name="Signal program 1">
      <sgs>
        <sg sg_id="1" signal_sequence="3">
          <cmds>
            <cmd display="3" begin="0" />
            <cmd display="1" begin="26000" />
          </cmds>
          <fixedstates>
            <fixedstate display="4" duration="3000" />
            <fixedstate display="2" duration="0" />
          </fixedstates>
        </sg>
        <sg sg_id="2" signal_sequence="3">
          <cmds>
            <cmd display="1" begin="0" />
            <cmd display="3" begin="26000" />
          </cmds>
          <fixedstates>
            <fixedstate display="2" duration="0" />
            <fixedstate display="4" duration="3000" />
          </fixedstates>
        </sg>
        <sg sg_id="3" signal_sequence="3">
          <cmds>
            <cmd display="3" begin="0" />
            <cmd display="1" begin="26000" />
          </cmds>
          <fixedstates>
            <fixedstate display="4" duration="3000" />
            <fixedstate display="2" duration="0" />
          </fixedstates>
        </sg>
        <sg sg_id="4" signal_sequence="3">
          <cmds>
            <cmd display="1" begin="0" />
            <cmd display="3" begin="26000" />
          </cmds>
          <fixedstates>
            <fixedstate display="2" duration="0" />
            <fixedstate display="4" duration="3000" />
          </fixedstates>
        </sg>
      </sgs>
    </prog>
    <prog id="2" cycletime="54000" switchpoint="0" offset="0" intergreens="0" fitness="0.000000" vehicleCount="0" name="Signal program 2">
      <sgs>
        <sg sg_id="1" signal_sequence="3">
          <cmds>
            <cmd display="3" begin="0" />
            <cmd display="1" begin="27000" />
          </cmds>
          <fixedstates>
            <fixedstate display="4" duration="3000" />
            <fixedstate display="2" duration="0" />
          </fixedstates>
        </sg>
        <sg sg_id="2" signal_sequence="3">
          <cmds>
            <cmd display="1" begin="0" />
            <cmd display="3" begin="27000" />
          </cmds>
          <fixedstates>
            <fixedstate display="2" duration="0" />
            <fixedstate display="4" duration="3000" />
          </fixedstates>
        </sg>
        <sg sg_id="3" signal_sequence="3">
          <cmds>
            <cmd display="3" begin="0" />
            <cmd display="1" begin="27000" />
          </cmds>
          <fixedstates>
            <fixedstate display="4" duration="3000" />
            <fixedstate display="2" duration="0" />
          </fixedstates>
        </sg>
        <sg sg_id="4" signal_sequence="3">
          <cmds>
            <cmd display="1" begin="0" />
            <cmd display="3" begin="27000" />
          </cmds>
          <fixedstates>
            <fixedstate display="2" duration="0" />
            <fixedstate display="4" duration="3000" />
          </fixedstates>
        </sg>
      </sgs>
    </prog>
    <prog id="3" cycletime="56000" switchpoint="0" offset="0" intergreens="0" fitness="0.000000" vehicleCount="0" name="Signal program 3">
      <sgs>
        <sg sg_id="1" signal_sequence="3">
          <cmds>
            <cmd display="3" begin="0" />
            <cmd display="1" begin="28000" />
          </cmds>
          <fixedstates>
            <fixedstate display="4" duration="3000" />
            <fixedstate display="2" duration="0" />
          </fixedstates>
        </sg>
        <sg sg_id="2" signal_sequence="3">
          <cmds>
            <cmd display="1" begin="0" />
            <cmd display="3" begin="28000" />
          </cmds>
          <fixedstates>
            <fixedstate display="2" duration="0" />
            <fixedstate display="4" duration="3000" />
          </fixedstates>
        </sg>
        <sg sg_id="3" signal_sequence="3">
          <cmds>
            <cmd display="3" begin="0" />
            <cmd display="1" begin="28000" />
          </cmds>
          <fixedstates>
            <fixedstate display="4" duration="3000" />
            <fixedstate display="2" duration="0" />
          </fixedstates>
        </sg>
        <sg sg_id="4" signal_sequence="3">
          <cmds>
            <cmd display="1" begin="0" />
            <cmd display="3" begin="28000" />
          </cmds>
          <fixedstates>
            <fixedstate display="2" duration="0" />
            <fixedstate display="4" duration="3000" />
          </fixedstates>
        </sg>
      </sgs>
    </prog>
    <prog id="4" cycletime="58000" switchpoint="0" offset="0" intergreens="0" fitness="0.000000" vehicleCount="0" name="Signal program 4">
      <sgs>
        <sg sg_id="1" signal_sequence="3">
          <cmds>
            <cmd display="3" begin="0" />
            <cmd display="1" begin="29000" />
          </cmds>
          <fixedstates>
            <fixedstate display="4" duration="3000" />
            <fixedstate display="2" duration="0" />
          </fixedstates>
        </sg>
        <sg sg_id="2" signal_sequence="3">
          <cmds>
            <cmd display="3" begin="0" />
            <cmd display="1" begin="29000" />
          </cmds>
          <fixedstates>
            <fixedstate display="4" duration="3000" />
            <fixedstate display="2" duration="0" />
          </fixedstates>
        </sg>
        <sg sg_id="3" signal_sequence="3">
          <cmds>
            <cmd display="3" begin="0" />
            <cmd display="1" begin="29000" />
          </cmds>
          <fixedstates>
            <fixedstate display="4" duration="3000" />
            <fixedstate display="2" duration="0" />
          </fixedstates>
        </sg>
        <sg sg_id="4" signal_sequence="3">
          <cmds>
            <cmd display="3" begin="0" />
            <cmd display="1" begin="29000" />
          </cmds>
          <fixedstates>
            <fixedstate display="4" duration="3000" />
            <fixedstate display="2" duration="0" />
          </fixedstates>
        </sg>
      </sgs>
    </prog>
    <prog id="5" cycletime="110000" switchpoint="0" offset="0" intergreens="0" fitness="0.000000" vehicleCount="0" name="Signal program 5">
      <sgs>
        <sg sg_id="1" signal_sequence="3">
          <cmds>
            <cmd display="3" begin="0" />
            <cmd display="1" begin="55000" />
          </cmds>
          <fixedstates>
            <fixedstate display="4" duration="3000" />
            <fixedstate display="2" duration="0" />
          </fixedstates>
        </sg>
        <sg sg_id="2" signal_sequence="3">
          <cmds>
            <cmd display="1" begin="0" />
            <cmd display="3" begin="55000" />
          </cmds>
          <fixedstates>
            <fixedstate display="2" duration="0" />
            <fixedstate display="4" duration="3000" />
          </fixedstates>
        </sg>
        <sg sg_id="3" signal_sequence="3">
          <cmds>
            <cmd display="3" begin="0" />
            <cmd display="1" begin="55000" />
          </cmds>
          <fixedstates>
            <fixedstate display="4" duration="3000" />
            <fixedstate display="2" duration="0" />
          </fixedstates>
        </sg>
        <sg sg_id="4" signal_sequence="3">
          <cmds>
            <cmd display="1" begin="0" />
            <cmd display="3" begin="55000" />
          </cmds>
          <fixedstates>
            <fixedstate display="2" duration="0" />
            <fixedstate display="4" duration="3000" />
          </fixedstates>
        </sg>
      </sgs>
    </prog>
  </progs>
  <stages>
    <stage id="1" name="Stage 1" isPseudoStage="false">
      <activations>
        <activation sg_id="1" activation="ON" />
        <activation sg_id="2" activation="OFF" />
        <activation sg_id="3" activation="ON" />
        <activation sg_id="4" activation="OFF" />
      </activations>
    </stage>
    <stage id="2" name="Stage 2" isPseudoStage="false">
      <activations>
        <activation sg_id="1" activation="OFF" />
        <activation sg_id="2" activation="ON" />
        <activation sg_id="3" activation="OFF" />
        <activation sg_id="4" activation="ON" />
      </activations>
    </stage>
  </stages>
  <interstageProgs />
  <stageProgs />
  <dailyProgLists />
</sc>