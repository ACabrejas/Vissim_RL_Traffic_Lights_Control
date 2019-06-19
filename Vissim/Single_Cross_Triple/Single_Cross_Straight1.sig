<?xml version="1.0" encoding="UTF-8"?>
<sc version="201801" id="3" name="" frequency="1" steps="0" defaultIntergreenMatrix="0" interstagesUsingMinDurations="true" checkSum="4216210356">
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
    <signalsequence id="1" name="Permanent Red">
      <state display="1" isFixedDuration="false" isClosed="true" defaultDuration="0" />
    </signalsequence>
    <signalsequence id="3" name="Red-Red/Amber-Green-Amber">
      <state display="1" isFixedDuration="false" isClosed="true" defaultDuration="1000" />
      <state display="2" isFixedDuration="true" isClosed="true" defaultDuration="1000" />
      <state display="3" isFixedDuration="false" isClosed="false" defaultDuration="5000" />
      <state display="4" isFixedDuration="true" isClosed="true" defaultDuration="3000" />
    </signalsequence>
  </signalsequences>
  <sgs>
    <sg id="1" name="West - Left" defaultSignalSequence="3">
      <defaultDurations>
        <defaultDuration display="1" duration="1000" />
        <defaultDuration display="2" duration="1000" />
        <defaultDuration display="3" duration="5000" />
        <defaultDuration display="4" duration="3000" />
      </defaultDurations>
    </sg>
    <sg id="2" name="West - Middle" defaultSignalSequence="3">
      <defaultDurations>
        <defaultDuration display="1" duration="1000" />
        <defaultDuration display="2" duration="1000" />
        <defaultDuration display="3" duration="5000" />
        <defaultDuration display="4" duration="3000" />
      </defaultDurations>
    </sg>
    <sg id="3" name="West - Right" defaultSignalSequence="3">
      <defaultDurations>
        <defaultDuration display="1" duration="1000" />
        <defaultDuration display="2" duration="1000" />
        <defaultDuration display="3" duration="5000" />
        <defaultDuration display="4" duration="3000" />
      </defaultDurations>
    </sg>
    <sg id="4" name="South - Left" defaultSignalSequence="3">
      <defaultDurations>
        <defaultDuration display="1" duration="1000" />
        <defaultDuration display="2" duration="1000" />
        <defaultDuration display="3" duration="5000" />
        <defaultDuration display="4" duration="3000" />
      </defaultDurations>
    </sg>
    <sg id="5" name="South - Middle" defaultSignalSequence="3">
      <defaultDurations>
        <defaultDuration display="1" duration="1000" />
        <defaultDuration display="2" duration="1000" />
        <defaultDuration display="3" duration="5000" />
        <defaultDuration display="4" duration="3000" />
      </defaultDurations>
    </sg>
    <sg id="6" name="South - Right" defaultSignalSequence="3">
      <defaultDurations>
        <defaultDuration display="1" duration="1000" />
        <defaultDuration display="2" duration="1000" />
        <defaultDuration display="3" duration="5000" />
        <defaultDuration display="4" duration="3000" />
      </defaultDurations>
    </sg>
    <sg id="7" name="East - Left" defaultSignalSequence="3">
      <defaultDurations>
        <defaultDuration display="1" duration="1000" />
        <defaultDuration display="2" duration="1000" />
        <defaultDuration display="3" duration="5000" />
        <defaultDuration display="4" duration="3000" />
      </defaultDurations>
    </sg>
    <sg id="8" name="East - Middle" defaultSignalSequence="3">
      <defaultDurations>
        <defaultDuration display="1" duration="1000" />
        <defaultDuration display="2" duration="1000" />
        <defaultDuration display="3" duration="5000" />
        <defaultDuration display="4" duration="3000" />
      </defaultDurations>
    </sg>
    <sg id="9" name="East - Right" defaultSignalSequence="3">
      <defaultDurations>
        <defaultDuration display="1" duration="1000" />
        <defaultDuration display="2" duration="1000" />
        <defaultDuration display="3" duration="5000" />
        <defaultDuration display="4" duration="3000" />
      </defaultDurations>
    </sg>
    <sg id="10" name="North - Left" defaultSignalSequence="3">
      <defaultDurations>
        <defaultDuration display="1" duration="1000" />
        <defaultDuration display="2" duration="1000" />
        <defaultDuration display="3" duration="5000" />
        <defaultDuration display="4" duration="3000" />
      </defaultDurations>
    </sg>
    <sg id="11" name="North - Middle" defaultSignalSequence="3">
      <defaultDurations>
        <defaultDuration display="1" duration="1000" />
        <defaultDuration display="2" duration="1000" />
        <defaultDuration display="3" duration="5000" />
        <defaultDuration display="4" duration="3000" />
      </defaultDurations>
    </sg>
    <sg id="12" name="North - Right" defaultSignalSequence="3">
      <defaultDurations>
        <defaultDuration display="1" duration="1000" />
        <defaultDuration display="2" duration="1000" />
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
    </intergreenmatrix>
  </intergreenmatrices>
  <progs>
    <prog id="1" cycletime="90000" switchpoint="0" offset="0" intergreens="0" fitness="0.000000" vehicleCount="0" name="Signal program 1">
      <sgs>
        <sg sg_id="1" signal_sequence="3">
          <cmds>
            <cmd display="1" begin="0" />
            <cmd display="3" begin="78000" />
          </cmds>
          <fixedstates>
            <fixedstate display="2" duration="1000" />
            <fixedstate display="4" duration="3000" />
          </fixedstates>
        </sg>
        <sg sg_id="2" signal_sequence="3">
          <cmds>
            <cmd display="3" begin="1000" />
            <cmd display="1" begin="77000" />
          </cmds>
          <fixedstates>
            <fixedstate display="2" duration="1000" />
            <fixedstate display="4" duration="3000" />
          </fixedstates>
        </sg>
        <sg sg_id="3" signal_sequence="3">
          <cmds>
            <cmd display="1" begin="0" />
            <cmd display="3" begin="78000" />
          </cmds>
          <fixedstates>
            <fixedstate display="2" duration="1000" />
            <fixedstate display="4" duration="3000" />
          </fixedstates>
        </sg>
        <sg sg_id="4" signal_sequence="3">
          <cmds>
            <cmd display="3" begin="1000" />
            <cmd display="1" begin="77000" />
          </cmds>
          <fixedstates>
            <fixedstate display="2" duration="1000" />
            <fixedstate display="4" duration="3000" />
          </fixedstates>
        </sg>
        <sg sg_id="5" signal_sequence="1">
          <cmds>
            <cmd display="1" begin="0" />
          </cmds>
          <fixedstates />
        </sg>
        <sg sg_id="6" signal_sequence="1">
          <cmds>
            <cmd display="1" begin="0" />
          </cmds>
          <fixedstates />
        </sg>
        <sg sg_id="7" signal_sequence="1">
          <cmds>
            <cmd display="1" begin="0" />
          </cmds>
          <fixedstates />
        </sg>
        <sg sg_id="8" signal_sequence="1">
          <cmds>
            <cmd display="1" begin="0" />
          </cmds>
          <fixedstates />
        </sg>
        <sg sg_id="9" signal_sequence="1">
          <cmds>
            <cmd display="1" begin="0" />
          </cmds>
          <fixedstates />
        </sg>
        <sg sg_id="10" signal_sequence="1">
          <cmds>
            <cmd display="1" begin="0" />
          </cmds>
          <fixedstates />
        </sg>
        <sg sg_id="11" signal_sequence="1">
          <cmds>
            <cmd display="1" begin="0" />
          </cmds>
          <fixedstates />
        </sg>
        <sg sg_id="12" signal_sequence="1">
          <cmds>
            <cmd display="1" begin="0" />
          </cmds>
          <fixedstates />
        </sg>
      </sgs>
    </prog>
    <prog id="2" cycletime="90000" switchpoint="0" offset="0" intergreens="0" fitness="0.000000" vehicleCount="0" name="Signal program 2">
      <sgs>
        <sg sg_id="1" signal_sequence="3">
          <cmds>
            <cmd display="1" begin="0" />
            <cmd display="3" begin="67000" />
          </cmds>
          <fixedstates>
            <fixedstate display="2" duration="1000" />
            <fixedstate display="4" duration="3000" />
          </fixedstates>
        </sg>
        <sg sg_id="2" signal_sequence="3">
          <cmds>
            <cmd display="3" begin="1000" />
            <cmd display="1" begin="66000" />
          </cmds>
          <fixedstates>
            <fixedstate display="2" duration="1000" />
            <fixedstate display="4" duration="3000" />
          </fixedstates>
        </sg>
        <sg sg_id="3" signal_sequence="3">
          <cmds>
            <cmd display="1" begin="0" />
            <cmd display="3" begin="67000" />
          </cmds>
          <fixedstates>
            <fixedstate display="2" duration="1000" />
            <fixedstate display="4" duration="3000" />
          </fixedstates>
        </sg>
        <sg sg_id="4" signal_sequence="3">
          <cmds>
            <cmd display="3" begin="1000" />
            <cmd display="1" begin="66000" />
          </cmds>
          <fixedstates>
            <fixedstate display="2" duration="1000" />
            <fixedstate display="4" duration="3000" />
          </fixedstates>
        </sg>
        <sg sg_id="5" signal_sequence="1">
          <cmds>
            <cmd display="1" begin="0" />
          </cmds>
          <fixedstates />
        </sg>
        <sg sg_id="6" signal_sequence="1">
          <cmds>
            <cmd display="1" begin="0" />
          </cmds>
          <fixedstates />
        </sg>
        <sg sg_id="7" signal_sequence="1">
          <cmds>
            <cmd display="1" begin="0" />
          </cmds>
          <fixedstates />
        </sg>
        <sg sg_id="8" signal_sequence="1">
          <cmds>
            <cmd display="1" begin="0" />
          </cmds>
          <fixedstates />
        </sg>
        <sg sg_id="9" signal_sequence="1">
          <cmds>
            <cmd display="1" begin="0" />
          </cmds>
          <fixedstates />
        </sg>
        <sg sg_id="10" signal_sequence="1">
          <cmds>
            <cmd display="1" begin="0" />
          </cmds>
          <fixedstates />
        </sg>
        <sg sg_id="11" signal_sequence="1">
          <cmds>
            <cmd display="1" begin="0" />
          </cmds>
          <fixedstates />
        </sg>
        <sg sg_id="12" signal_sequence="1">
          <cmds>
            <cmd display="1" begin="0" />
          </cmds>
          <fixedstates />
        </sg>
      </sgs>
    </prog>
    <prog id="3" cycletime="90000" switchpoint="0" offset="0" intergreens="0" fitness="0.000000" vehicleCount="0" name="Signal program 3">
      <sgs>
        <sg sg_id="1" signal_sequence="3">
          <cmds>
            <cmd display="1" begin="0" />
            <cmd display="3" begin="46000" />
          </cmds>
          <fixedstates>
            <fixedstate display="2" duration="1000" />
            <fixedstate display="4" duration="3000" />
          </fixedstates>
        </sg>
        <sg sg_id="2" signal_sequence="3">
          <cmds>
            <cmd display="3" begin="1000" />
            <cmd display="1" begin="45000" />
          </cmds>
          <fixedstates>
            <fixedstate display="2" duration="1000" />
            <fixedstate display="4" duration="3000" />
          </fixedstates>
        </sg>
        <sg sg_id="3" signal_sequence="3">
          <cmds>
            <cmd display="1" begin="0" />
            <cmd display="3" begin="46000" />
          </cmds>
          <fixedstates>
            <fixedstate display="2" duration="1000" />
            <fixedstate display="4" duration="3000" />
          </fixedstates>
        </sg>
        <sg sg_id="4" signal_sequence="3">
          <cmds>
            <cmd display="3" begin="1000" />
            <cmd display="1" begin="45000" />
          </cmds>
          <fixedstates>
            <fixedstate display="2" duration="1000" />
            <fixedstate display="4" duration="3000" />
          </fixedstates>
        </sg>
        <sg sg_id="5" signal_sequence="1">
          <cmds>
            <cmd display="1" begin="0" />
          </cmds>
          <fixedstates />
        </sg>
        <sg sg_id="6" signal_sequence="1">
          <cmds>
            <cmd display="1" begin="0" />
          </cmds>
          <fixedstates />
        </sg>
        <sg sg_id="7" signal_sequence="1">
          <cmds>
            <cmd display="1" begin="0" />
          </cmds>
          <fixedstates />
        </sg>
        <sg sg_id="8" signal_sequence="1">
          <cmds>
            <cmd display="1" begin="0" />
          </cmds>
          <fixedstates />
        </sg>
        <sg sg_id="9" signal_sequence="1">
          <cmds>
            <cmd display="1" begin="0" />
          </cmds>
          <fixedstates />
        </sg>
        <sg sg_id="10" signal_sequence="1">
          <cmds>
            <cmd display="1" begin="0" />
          </cmds>
          <fixedstates />
        </sg>
        <sg sg_id="11" signal_sequence="1">
          <cmds>
            <cmd display="1" begin="0" />
          </cmds>
          <fixedstates />
        </sg>
        <sg sg_id="12" signal_sequence="1">
          <cmds>
            <cmd display="1" begin="0" />
          </cmds>
          <fixedstates />
        </sg>
      </sgs>
    </prog>
    <prog id="4" cycletime="90000" switchpoint="0" offset="0" intergreens="0" fitness="0.000000" vehicleCount="0" name="Signal program 4">
      <sgs>
        <sg sg_id="1" signal_sequence="3">
          <cmds>
            <cmd display="1" begin="0" />
            <cmd display="3" begin="25000" />
          </cmds>
          <fixedstates>
            <fixedstate display="2" duration="1000" />
            <fixedstate display="4" duration="3000" />
          </fixedstates>
        </sg>
        <sg sg_id="2" signal_sequence="3">
          <cmds>
            <cmd display="3" begin="1000" />
            <cmd display="1" begin="24000" />
          </cmds>
          <fixedstates>
            <fixedstate display="2" duration="1000" />
            <fixedstate display="4" duration="3000" />
          </fixedstates>
        </sg>
        <sg sg_id="3" signal_sequence="3">
          <cmds>
            <cmd display="1" begin="0" />
            <cmd display="3" begin="25000" />
          </cmds>
          <fixedstates>
            <fixedstate display="2" duration="1000" />
            <fixedstate display="4" duration="3000" />
          </fixedstates>
        </sg>
        <sg sg_id="4" signal_sequence="3">
          <cmds>
            <cmd display="3" begin="1000" />
            <cmd display="1" begin="24000" />
          </cmds>
          <fixedstates>
            <fixedstate display="2" duration="1000" />
            <fixedstate display="4" duration="3000" />
          </fixedstates>
        </sg>
        <sg sg_id="5" signal_sequence="1">
          <cmds>
            <cmd display="1" begin="0" />
          </cmds>
          <fixedstates />
        </sg>
        <sg sg_id="6" signal_sequence="1">
          <cmds>
            <cmd display="1" begin="0" />
          </cmds>
          <fixedstates />
        </sg>
        <sg sg_id="7" signal_sequence="1">
          <cmds>
            <cmd display="1" begin="0" />
          </cmds>
          <fixedstates />
        </sg>
        <sg sg_id="8" signal_sequence="1">
          <cmds>
            <cmd display="1" begin="0" />
          </cmds>
          <fixedstates />
        </sg>
        <sg sg_id="9" signal_sequence="1">
          <cmds>
            <cmd display="1" begin="0" />
          </cmds>
          <fixedstates />
        </sg>
        <sg sg_id="10" signal_sequence="1">
          <cmds>
            <cmd display="1" begin="0" />
          </cmds>
          <fixedstates />
        </sg>
        <sg sg_id="11" signal_sequence="1">
          <cmds>
            <cmd display="1" begin="0" />
          </cmds>
          <fixedstates />
        </sg>
        <sg sg_id="12" signal_sequence="1">
          <cmds>
            <cmd display="1" begin="0" />
          </cmds>
          <fixedstates />
        </sg>
      </sgs>
    </prog>
    <prog id="5" cycletime="90000" switchpoint="0" offset="0" intergreens="0" fitness="0.000000" vehicleCount="0" name="Signal program 5">
      <sgs>
        <sg sg_id="1" signal_sequence="3">
          <cmds>
            <cmd display="1" begin="0" />
            <cmd display="3" begin="14000" />
          </cmds>
          <fixedstates>
            <fixedstate display="2" duration="1000" />
            <fixedstate display="4" duration="3000" />
          </fixedstates>
        </sg>
        <sg sg_id="2" signal_sequence="3">
          <cmds>
            <cmd display="3" begin="1000" />
            <cmd display="1" begin="13000" />
          </cmds>
          <fixedstates>
            <fixedstate display="2" duration="1000" />
            <fixedstate display="4" duration="3000" />
          </fixedstates>
        </sg>
        <sg sg_id="3" signal_sequence="3">
          <cmds>
            <cmd display="1" begin="0" />
            <cmd display="3" begin="14000" />
          </cmds>
          <fixedstates>
            <fixedstate display="2" duration="1000" />
            <fixedstate display="4" duration="3000" />
          </fixedstates>
        </sg>
        <sg sg_id="4" signal_sequence="3">
          <cmds>
            <cmd display="3" begin="1000" />
            <cmd display="1" begin="13000" />
          </cmds>
          <fixedstates>
            <fixedstate display="2" duration="1000" />
            <fixedstate display="4" duration="3000" />
          </fixedstates>
        </sg>
        <sg sg_id="5" signal_sequence="1">
          <cmds>
            <cmd display="1" begin="0" />
          </cmds>
          <fixedstates />
        </sg>
        <sg sg_id="6" signal_sequence="1">
          <cmds>
            <cmd display="1" begin="0" />
          </cmds>
          <fixedstates />
        </sg>
        <sg sg_id="7" signal_sequence="1">
          <cmds>
            <cmd display="1" begin="0" />
          </cmds>
          <fixedstates />
        </sg>
        <sg sg_id="8" signal_sequence="1">
          <cmds>
            <cmd display="1" begin="0" />
          </cmds>
          <fixedstates />
        </sg>
        <sg sg_id="9" signal_sequence="1">
          <cmds>
            <cmd display="1" begin="0" />
          </cmds>
          <fixedstates />
        </sg>
        <sg sg_id="10" signal_sequence="1">
          <cmds>
            <cmd display="1" begin="0" />
          </cmds>
          <fixedstates />
        </sg>
        <sg sg_id="11" signal_sequence="1">
          <cmds>
            <cmd display="1" begin="0" />
          </cmds>
          <fixedstates />
        </sg>
        <sg sg_id="12" signal_sequence="1">
          <cmds>
            <cmd display="1" begin="0" />
          </cmds>
          <fixedstates />
        </sg>
      </sgs>
    </prog>
  </progs>
  <stages />
  <interstageProgs />
  <stageProgs />
  <dailyProgLists />
</sc>