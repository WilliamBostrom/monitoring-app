<script lang="ts">
  import '../app.css'
	let { children } = $props();
</script>

<header class="header">
  <div class="header-content">
    <h1 class="header-title">Raspberry Pi Systemövervakning</h1>
  </div>
</header>

<main class="main-content">
  {@render children?.()}
</main>

<style>
  /* Header-stil */
  .header {
    background: linear-gradient(135deg, #0d1117 0%, #161b22 50%, #21262d 100%);
    color: #f0f6fc;
    padding: 1rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1);
    width: 100%;
    margin: 0;
    position: relative;
    border-bottom: 1px solid #30363d;
  }

  .header-content {
    display: flex;
    align-items: center;
  }

  .header-title {
    font-size: 1.5rem;
    font-weight: 600;
    margin: 0;
    color: #f0f6fc;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
    font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  }

  /* Main-yta under headern */
  .main-content {
    padding: 2rem;
    background-color: #1a1a1a;
    min-height: calc(100vh - 70px);
  }
</style>


