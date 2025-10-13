<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import * as api from '../lib/api.js';

  let menuBtns: any[] = [];
  let result: any = null;
  let monitoring: any = null;

  let loading = false;
  let initialLoading = true;
  let showAlarmInputs = false;
  let showAlarmList = false;
  let alarmType = "CPU användning";
  let threshold = 50;
  let monitoringInterval: any = null;

  // Alarm state
  let activeAlarms: any[] = [];
  let triggeredAlarms: any[] = [];
  let alarmMonitoringActive = false;
  let alarmMonitoringInterval: any = null;

  async function fetchMenu() {
    try {
      menuBtns = await api.fetchMenu();
    } catch (err: any) {
      console.error('Error loading menu:', err.message);
    } finally {
      initialLoading = false;
    }
  }

  async function selectChoice(id: any) {
    loading = true;
    result = null;
    
    try {
      if (id === 3) {
        showAlarmInputs = true;
        return;
      }

      if (id === 1) {
        activeMonitoring(id);
        return;
      }

      if (id === 4) {
        await fetchAlarms();
        showAlarmInputs = false;
        showAlarmList = !showAlarmList;
        return;
      }

      if (id === 5) {
        await startAlarmMonitoring();
        return;
      }

      if (id === 6) {
        stopAllMonitoring();
        return;
      }

      // For other choices, use the API
      result = await api.selectChoice(id);
    } catch (err: any) {
      console.error('Error in selectChoice:', err.message);
      result = "Ett fel uppstod: " + err.message;
    } finally {
      loading = false;
    }
  }

  async function activeMonitoring(id: any) {
    if (monitoringInterval) {
      clearInterval(monitoringInterval);
    }
    
    monitoringInterval = setInterval(async () => {
      try {
        monitoring = await api.selectChoice(id);
      } catch (err: any) {
        console.error('Fel vid övervakning:', err.message);
        monitoring = "Ett fel uppstod vid övervakning: " + err.message;
      }
    }, 1000);
  }

  function stopAllMonitoring() {
    if (monitoringInterval) {
      clearInterval(monitoringInterval);
      monitoringInterval = null;
    }
    
    if (alarmMonitoringInterval) {
      clearInterval(alarmMonitoringInterval);
      alarmMonitoringInterval = null;
    }
    
    if (alarmMonitoringActive) {
      stopAlarmMonitoring();
    }
    
    monitoring = null;
    result = null;
    alarmMonitoringActive = false;
    triggeredAlarms = [];
    
  }

  async function submitAlarm(event: SubmitEvent) {
    event.preventDefault();
    loading = true;
    
    try {
      const data = await api.createAlarm(alarmType, threshold);
      
      if (data.error) {
        result = data.error;
      } else {
        await fetchAlarms();
        showAlarmInputs = false;
        result = data.message;
      }
    } catch (err: any) {
      console.error("Error creating alarm:", err);
      result = "Ett fel uppstod: " + err.message;
    } finally {
      loading = false;
    }
  }

  async function fetchAlarms() {
    try {
      activeAlarms = await api.fetchAlarms();
    } catch (err: any) {
      console.error("Fel vid hämtning av alarm:", err.message);
    }
  }

  async function fetchAlarmStatus() {
    try {
      const data = await api.fetchAlarmStatus();
      triggeredAlarms = data.triggered_alarms || [];
      alarmMonitoringActive = data.monitoring_active;
    } catch (err: any) {
      console.error("Fel vid hämtning av alarm status:", err.message);
    }
  }

  async function startAlarmMonitoring() {
    try {
      const data = await api.startAlarmMonitoring();
      
      if (data.message) {
        alarmMonitoringActive = true;
        alarmMonitoringInterval = setInterval(fetchAlarmStatus, 2000);
        result = data.message;
      }
    } catch (err: any) {
      console.error("Fel vid start av alarm monitoring:", err.message);
      result = "Ett fel uppstod: " + err.message;
    }
  }

  async function stopAlarmMonitoring() {
    try {
      const data = await api.stopAlarmMonitoring();
      
      if (data.message) {
        alarmMonitoringActive = false;
        if (alarmMonitoringInterval) {
          clearInterval(alarmMonitoringInterval);
          alarmMonitoringInterval = null;
        }
        result = data.message;
      }
    } catch (err: any) {
      console.error("Fel vid stopp av alarm monitoring:", err.message);
      result = "Ett fel uppstod: " + err.message;
    }
  }

  async function deleteAlarm(alarmId: number) {
    try {
      const data = await api.deleteAlarm(alarmId);
      
      if (data.message) {
        await fetchAlarms();
        result = data.message;
      } else {
        result = data.error;
      }
    } catch (err: any) {
      console.error("Fel vid borttagning av alarm:", err.message);
      result = "Ett fel uppstod: " + err.message;
    }
  }

  onMount(async () => {
    await fetchMenu();
    await fetchAlarms();
    await fetchAlarmStatus();
  });

  onDestroy(() => {
    if (monitoringInterval) {
      clearInterval(monitoringInterval);
    }
    if (alarmMonitoringInterval) {
      clearInterval(alarmMonitoringInterval);
    }
  });
</script>

{#if initialLoading}
  <div class="loading-container">
    <div class="loading-spinner"></div>
    <p>Laddar meny...</p>
  </div>
{:else if alarmMonitoringActive}
  <!-- Monitoring Mode - Visa bara alarm-relaterad information -->
  <div class="monitoring-mode">
    <!-- Visa aktiva alarm -->
    {#if activeAlarms.length > 0}
    <div class="alarms-container">
        <div class="alarms-header">
            <h3>🔍 Övervakningsläge aktivt - Aktiva larm ({activeAlarms.length})</h3>
            <button class="btn btn-danger" onclick={stopAlarmMonitoring}>Stoppa övervakning</button>
        </div>
        <ul class="alarms-list">
            {#each activeAlarms as alarm}
                <li class="alarm-item">
                    <div class="alarm-info">
                        <span class="alarm-type">{alarm.type}</span>
                        <span class="alarm-threshold">{alarm.threshold}%</span>
                    </div>
                    <button class="btn btn-danger" onclick={() => deleteAlarm(alarm.id)}>Ta bort</button>
                </li>
            {/each}
        </ul>
    </div>
    {:else}
    <div class="no-alarms">
        <h3>🔍 Övervakningsläge aktivt</h3>
        <p>Inga aktiva larm konfigurerade.</p>
        <button class="btn btn-danger" onclick={stopAlarmMonitoring}>Stoppa övervakning</button>
    </div>
    {/if}

    <!-- Visa triggade alarm -->
    {#if triggeredAlarms.length > 0}
    <div class="triggered-alarms-container">
        <h3>🚨 TRIGGADE LARM ({triggeredAlarms.length})</h3>
        <ul class="triggered-alarms-list">
            {#each triggeredAlarms as triggered}
                <li class="triggered-alarm-item">
                    <div class="alarm-warning">
                        <span class="warning-text">VARNING: {triggered.alarm.type} ÖVERSTIGER {triggered.threshold}%</span>
                        <span class="current-value">Aktuellt värde: {triggered.current_value.toFixed(1)}%</span>
                    </div>
                </li>
            {/each}
        </ul>
    </div>
    {:else}
    <div class="no-triggered-alarms">
        <p>✅ Inga larm triggade för tillfället</p>
    </div>
    {/if}
  </div>
{:else}
  <!-- Normal Mode - Visa meny och allt annat -->
  <div class="btn-container">
      {#each menuBtns as btn }
     <button class="btn" onclick={()=> selectChoice(btn.id)} disabled={loading}>
       {#if loading}
         <span class="loading-spinner" ></span>
       {:else if btn.id === 1 && monitoring && typeof monitoring === 'object'}
         <div class="btn-content">
           <div class="btn-title">{btn.text}</div>
           <div class="btn-values">
             <span>CPU: {monitoring.cpu_percent}%</span>
             <span>RAM: {monitoring.memory_percent}%</span>
             <span>Disk: {monitoring.disk_percent}%</span>
           </div>
         </div>
       {:else if btn.id === 2 && result && typeof result === 'object'}
         <div class="btn-content">
           <div class="btn-title">{btn.text}</div>
           <div class="btn-values">
             <span>CPU: {result.cpu_percent}%</span>
             <span>RAM: {result.memory_percent}%</span>
             <span>Disk: {result.disk_percent}%</span>
           </div>
         </div>
       {:else if btn.id === 4 && activeAlarms.length > 0}
         <div class="btn-content">
           <div class="btn-title">{btn.text}</div>
           <div class="btn-values">
             <span>{activeAlarms.length} alarm aktiva</span>
           </div>
         </div>
       {:else}
         {btn.text}
       {/if}
     </button>
      {/each}
  </div>
{/if}

{#if result && !showAlarmInputs && (typeof result === 'string' && result.includes('fel') || typeof result === 'string' && result.includes('error'))}
  <div class="result-container">
    <div class="result-header">
      <h3>Fel:</h3>   
    </div>
    <div class="result-content">
      <p>{result}</p>
    </div>
  </div>
{/if}

{#if showAlarmInputs && !alarmMonitoringActive}
<div class="alarm-inputs">
  <form onsubmit={submitAlarm}>
    <label>
        Typ:
        <select bind:value={alarmType}>
            <option>CPU användning</option>
            <option>Minnesanvändning</option>
            <option>Diskanvändning</option>
        </select>
    </label>
  
    <label>
        Threshold (%):
        <input type="number" min="1" max="100" bind:value={threshold} />
    </label>
  
    <button type="submit">Skapa larm</button>
  </form>
</div>
{/if}

{#if activeAlarms.length > 0 && !alarmMonitoringActive && !showAlarmInputs && showAlarmList}
<div class="alarms-container">
  <h3>Aktiva larm ({activeAlarms.length}):</h3>
  <ul class="alarms-list">
    {#each activeAlarms as alarm}
      <li class="alarm-item">
        <div class="alarm-info">
          <span class="alarm-type">{alarm.type}</span>
          <span class="alarm-threshold">{alarm.threshold}%</span>
        </div>
        <button class="btn btn-danger" onclick={() => deleteAlarm(alarm.id)}>Ta bort</button>
      </li>
    {/each}
  </ul>
</div>
{/if}