<script lang="ts">
  import '../app.css'
	let { children } = $props();
</script>

<header class="header">
  <div class="header-content">
    <h1 class="header-title">Slutuppgift Python</h1>
  </div>
</header>

<main class="main-content">
  {@render children?.()}
</main>

<style>
  /* Header-stil */
  .header {
    background-color: #1b3d2f; /* mörkgrön ton */
    color: white;
    padding: 1rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
    width: 100%;
    margin: 0;
    position: relative;
  }

  .header-content {
    display: flex;
    align-items: center;
  }

  .header-title {
    font-size: 1.5rem;
    font-weight: 600;
    margin: 0;
  }

  /* Main-yta under headern */
  .main-content {
    padding: 2rem;
    background-color: #1a1a1a;
    min-height: calc(100vh - 70px);
  }
</style>


