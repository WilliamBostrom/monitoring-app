<script lang="ts">
  let menuBtns:any[] = [];
  let alarms:any[] = [];
  let result: any = null;
  let loading = false;
  let showAlarmInputs = false;
  let alarmType = "CPU användning";
  let threshold = 50;

  async function fetchMenu(){
    try {
      const res = await fetch("http://localhost:8000/menu");
      let data = await res.json()
      menuBtns = data.options;
      console.log(menuBtns)
    } catch(err: any){
      console.log(err.message)
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
      const res = await fetch("http://localhost:8000/select", {
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
        const res = await fetch("http://localhost:8000/set_alarm/3", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                type: alarmType,
                threshold: threshold
            })
        });
        const data = await res.json();
        alarms.push(data);
        console.log("Alarm created:", data);
        console.log("All alarms:", alarms);
        showAlarmInputs = false; // göm input-fälten efter submit
        result = `Larm skapat: ${data.message || 'Larm skapat framgångsrikt'}`;
    } catch (err: any) {
        console.error("Error creating alarm:", err);
        result = "Ett fel uppstod: " + err.message;
    } finally {
        loading = false;
    }
  }

  fetchMenu()

</script>

<h1>Raspberry Pi Systemövervakning</h1>

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
  h1 {
    text-align: center;
    color: #1b3d2f;
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 3rem;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  .btn-container {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1.5rem;
    flex-wrap: wrap;
    margin-top: 2rem;
  }

  .btns {
    background: linear-gradient(135deg, #1b3d2f 0%, #2d5a47 100%);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 1rem 2rem;
    font-size: 1.1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(27, 61, 47, 0.3);
    min-width: 150px;
    text-align: center;
    position: relative;
    overflow: hidden;
  }

  .btns::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
    transition: left 0.5s;
  }

  .btns:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(27, 61, 47, 0.4);
    background: linear-gradient(135deg, #2d5a47 0%, #1b3d2f 100%);
  }

  .btns:hover::before {
    left: 100%;
  }

  .btns:active {
    transform: translateY(-1px);
    box-shadow: 0 4px 15px rgba(27, 61, 47, 0.3);
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
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-radius: 50%;
    border-top-color: white;
    animation: spin 1s ease-in-out infinite;
    margin-right: 8px;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  .result-container {
    margin-top: 3rem;
    padding: 2rem;
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    border-left: 4px solid #1b3d2f;
  }

  .result-container h3 {
    color: #1b3d2f;
    margin-bottom: 1rem;
    font-size: 1.3rem;
  }

  .result-content p {
    font-size: 1.1rem;
    line-height: 1.6;
    color: #333;
  }

  .result-content ul {
    list-style: none;
    padding: 0;
  }

  .result-content li {
    padding: 0.5rem 0;
    border-bottom: 1px solid #eee;
    font-size: 1rem;
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
    background: #f8f9fa;
    border-radius: 8px;
    border-left: 3px solid #1b3d2f;
  }

  .info-item .label {
    font-weight: 600;
    color: #1b3d2f;
  }

  .info-item .value {
    font-weight: 700;
    font-size: 1.2rem;
    color: #2d5a47;
  }

  .alarm-inputs {
    margin-top: 2rem;
    padding: 2rem;
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    border-left: 4px solid #1b3d2f;
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
    color: #1b3d2f;
  }

  .alarm-inputs select,
  .alarm-inputs input {
    padding: 0.8rem;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    font-size: 1rem;
    transition: border-color 0.3s ease;
  }

  .alarm-inputs select:focus,
  .alarm-inputs input:focus {
    outline: none;
    border-color: #1b3d2f;
  }

  .alarm-inputs button {
    background: linear-gradient(135deg, #1b3d2f 0%, #2d5a47 100%);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 1rem 2rem;
    font-size: 1.1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    align-self: flex-start;
  }

  .alarm-inputs button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(27, 61, 47, 0.3);
  }

  .alarms-container {
    margin-top: 2rem;
    padding: 2rem;
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    border-left: 4px solid #e74c3c;
  }

  .alarms-container h3 {
    color: #e74c3c;
    margin-bottom: 1rem;
    font-size: 1.3rem;
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
    background: #fef2f2;
    border-radius: 8px;
    margin-bottom: 0.5rem;
    border-left: 3px solid #e74c3c;
  }

  .alarm-item:last-child {
    margin-bottom: 0;
  }

  .alarm-type {
    font-weight: 600;
    color: #1b3d2f;
  }

  .alarm-threshold {
    font-weight: 700;
    color: #e74c3c;
    font-size: 1.1rem;
  }

  /* Responsiv design */
  @media (max-width: 768px) {
    h1 {
      font-size: 2rem;
      margin-bottom: 2rem;
    }
    
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