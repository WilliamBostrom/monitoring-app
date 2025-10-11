<script lang="ts">
	import { onMount } from 'svelte';
	import { API_URL } from '../config.js';

  let menuBtns:any[] = [];
  let alarms:any[] = [];
  let result: any = null;
  let loading = false;
  let initialLoading = true;
  let showAlarmInputs = false;
  let alarmType = "CPU användning";
  let threshold = 50;

  async function fetchMenu(){
    try {
      const res = await fetch(`${API_URL}/menu`);
      let data = await res.json()
      menuBtns = data.options;
      console.log(menuBtns)
    } catch(err: any){
      console.log(err.message)
      console.log(err)
    } finally {
      initialLoading = false;
    }
  }

  async function selectChoice(id: any){
    loading = true;
    result = null;
    
    if (id === 3) {
        showAlarmInputs = true;
        loading = false;
        return;
    }

    try {
      const res = await fetch(`${API_URL}/select`, {
        method: 'POST',
        body: JSON.stringify({choice: id}),
        headers: {"Content-Type": "application/json",}
      });
      let data = await res.json()
      
      result = data.result;
      console.log(data)
    } catch(err: any){
      console.log(err.message)
      result = "Ett fel uppstod: " + err.message;
    } finally {
      loading = false;
    }
  }

  async function submitAlarm(event: SubmitEvent) {
    event.preventDefault();
    loading = true;
    try {
        const res = await fetch(`${API_URL}/set_alarm/3`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                type: alarmType,
                threshold: threshold
            })
        });
        const data = await res.json();
        alarms.push(data);
        showAlarmInputs = false; // göm input-fälten efter submit
        result = `Larm skapat: ${data.message || 'Larm skapat framgångsrikt'}`;
    } catch (err: any) {
        console.error("Error creating alarm:", err);
        result = "Ett fel uppstod: " + err.message;
    } finally {
        loading = false;
    }
  }

  onMount(() =>
  fetchMenu()
)


</script>

{#if initialLoading}
  <div class="loading-container">
    <div class="loading-spinner"></div>
    <p>Laddar meny...</p>
  </div>
{:else}
  <div class="btn-container">
      {#each menuBtns as btn }
     <button class="btns" onclick={()=> selectChoice(btn.id)} disabled={loading}>
       {#if loading}
         <span class="loading-spinner" ></span>
       {/if}
       {btn.text}
     </button>
      {/each}
  </div>
{/if}

{#if result}
  <div class="result-container">
    <h3>Resultat:</h3>
    <div class="result-content">
      {#if typeof result === 'string'}
        <p>{result}</p>
      {:else if Array.isArray(result)}
        <ul>
          {#each result as item}
            <li>{item}</li>
          {/each}
        </ul>
      {:else if typeof result === 'object'}
        <div class="system-info">
          <div class="info-item">
            <span class="label">CPU:</span>
            <span class="value">{result.cpu_percent}%</span>
          </div>
          <div class="info-item">
            <span class="label">Minne:</span>
            <span class="value">{result.memory_percent}%</span>
          </div>
          <div class="info-item">
            <span class="label">Disk:</span>
            <span class="value">{result.disk_percent}%</span>
          </div>
        </div>
      {/if}
    </div>
  </div>
{/if}

{#if showAlarmInputs}
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

{#if alarms.length > 0}
<div class="alarms-container">
  <h3>Aktiva larm:</h3>
  <ul class="alarms-list">
    {#each alarms as alarm}
      <li class="alarm-item">
        <span class="alarm-type">{alarm.type || alarmType}</span>
        <span class="alarm-threshold">{alarm.threshold || threshold}%</span>
      </li>
    {/each}
  </ul>
</div>
{/if}
<style>

  .btn-container {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1.5rem;
    flex-wrap: wrap;
    margin-top: 2rem;
  }

  .btns {
    background: linear-gradient(135deg, #0d4f3c 0%, #1a5a47 100%);
    color: #00ff41;
    border: 2px solid #00ff41;
    border-radius: 8px;
    padding: 1rem 2rem;
    font-size: 1.1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 0 15px rgba(0, 255, 65, 0.2);
    min-width: 150px;
    text-align: center;
    position: relative;
    overflow: hidden;
    font-family: 'Courier New', monospace;
  }

  .btns::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(0, 255, 65, 0.3), transparent);
    transition: left 0.5s;
  }

  .btns:hover {
    transform: translateY(-3px);
    box-shadow: 0 0 25px rgba(0, 255, 65, 0.4);
    background: linear-gradient(135deg, #1a5a47 0%, #0d4f3c 100%);
    border-color: #00ff88;
    color: #00ff88;
  }

  .btns:hover::before {
    left: 100%;
  }

  .btns:active {
    transform: translateY(-1px);
    box-shadow: 0 0 15px rgba(0, 255, 65, 0.3);
  }

  .btns:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
  }

  .loading-spinner {
    display: inline-block;
    width: 16px;
    height: 16px;
    border: 2px solid rgba(0, 255, 65, 0.3);
    border-radius: 50%;
    border-top-color: #00ff41;
    animation: spin 1s ease-in-out infinite;
    margin-right: 8px;
  }

  .loading-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 3rem;
    margin-top: 2rem;
  }

  .loading-container .loading-spinner {
    width: 32px;
    height: 32px;
    margin-right: 0;
    margin-bottom: 1rem;
  }

  .loading-container p {
    color: #00ff88;
    font-size: 1.1rem;
    font-family: 'Courier New', monospace;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  .result-container {
    margin-top: 3rem;
    padding: 2rem;
    background: #2a2a2a;
    border-radius: 8px;
    box-shadow: 0 0 20px rgba(0, 255, 65, 0.1);
    border: 2px solid #00ff41;
    font-family: 'Courier New', monospace;
  }

  .result-container h3 {
    color: #00ff41;
    margin-bottom: 1rem;
    font-size: 1.3rem;
    text-shadow: 0 0 5px rgba(0, 255, 65, 0.3);
  }

  .result-content p {
    font-size: 1.1rem;
    line-height: 1.6;
    color: #00ff88;
  }

  .result-content ul {
    list-style: none;
    padding: 0;
  }

  .result-content li {
    padding: 0.5rem 0;
    border-bottom: 1px solid #444;
    font-size: 1rem;
    color: #00ff88;
  }

  .result-content li:last-child {
    border-bottom: none;
  }

  .system-info {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
  }

  .info-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    background: #333;
    border-radius: 8px;
    border-left: 3px solid #00ff41;
  }

  .info-item .label {
    font-weight: 600;
    color: #00ff41;
  }

  .info-item .value {
    font-weight: 700;
    font-size: 1.2rem;
    color: #00ff88;
  }

  .alarm-inputs {
    margin-top: 2rem;
    padding: 2rem;
    background: #2a2a2a;
    border-radius: 8px;
    box-shadow: 0 0 20px rgba(0, 255, 65, 0.1);
    border: 2px solid #00ff41;
    font-family: 'Courier New', monospace;
  }

  .alarm-inputs form {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }

  .alarm-inputs label {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    font-weight: 600;
    color: #00ff41;
  }

  .alarm-inputs select,
  .alarm-inputs input {
    padding: 0.8rem;
    border: 2px solid #444;
    border-radius: 8px;
    font-size: 1rem;
    background: #1a1a1a;
    color: #00ff88;
    transition: border-color 0.3s ease;
    font-family: 'Courier New', monospace;
  }

  .alarm-inputs select:focus,
  .alarm-inputs input:focus {
    outline: none;
    border-color: #00ff41;
    box-shadow: 0 0 10px rgba(0, 255, 65, 0.2);
  }

  .alarm-inputs button {
    background: linear-gradient(135deg, #0d4f3c 0%, #1a5a47 100%);
    color: #00ff41;
    border: 2px solid #00ff41;
    border-radius: 8px;
    padding: 1rem 2rem;
    font-size: 1.1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    align-self: flex-start;
    font-family: 'Courier New', monospace;
  }

  .alarm-inputs button:hover {
    transform: translateY(-2px);
    box-shadow: 0 0 15px rgba(0, 255, 65, 0.3);
    border-color: #00ff88;
    color: #00ff88;
  }

  .alarms-container {
    margin-top: 2rem;
    padding: 2rem;
    background: #2a2a2a;
    border-radius: 8px;
    box-shadow: 0 0 20px rgba(255, 0, 0, 0.1);
    border: 2px solid #ff4444;
    font-family: 'Courier New', monospace;
  }

  .alarms-container h3 {
    color: #ff4444;
    margin-bottom: 1rem;
    font-size: 1.3rem;
    text-shadow: 0 0 5px rgba(255, 68, 68, 0.3);
  }

  .alarms-list {
    list-style: none;
    padding: 0;
    margin: 0;
  }

  .alarm-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    background: #333;
    border-radius: 8px;
    margin-bottom: 0.5rem;
    border-left: 3px solid #ff4444;
  }

  .alarm-item:last-child {
    margin-bottom: 0;
  }

  .alarm-type {
    font-weight: 600;
    color: #00ff41;
  }

  .alarm-threshold {
    font-weight: 700;
    color: #ff4444;
    font-size: 1.1rem;
  }

  /* Responsiv design */
  @media (max-width: 768px) {
    
    .btn-container {
      gap: 1rem;
      padding: 0 1rem;
    }
    
    .btns {
      padding: 0.8rem 1.5rem;
      font-size: 1rem;
      min-width: 120px;
    }
  }
</style>