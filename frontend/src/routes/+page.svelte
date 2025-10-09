<script lang="ts">
  let menuBtns:any[] = [];
  let result: any = null;
  let loading = false;

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