<template>
    <div id="search-component">
      <input v-model="query" placeholder="Digite o texto para buscar" />
      <button @click="buscarOperadoras">Buscar</button>
      
      <p v-if="carregando">Carregando...</p>
      
      <ul v-if="resultados.length">
        <li v-for="(operadora, index) in resultados" :key="index">
          {{ operadora.Razao_Social }} - {{ operadora.CNPJ }}
        </li>
      </ul>
      
      <p v-else-if="resultados.length === 0 && !carregando">Nenhum resultado encontrado.</p>
      </div>
      <p v-if="erro" class="error">{{ erro }}</p>
  </template>

  <script>
  import axios from "axios";
  
// este componente é responsável por buscar as operadoras no backend
  export default {
    data() {
      return {
        query: "",
        resultados: [],
        carregando: false,
        erro: "",
      };
    },
    methods: {
      async buscarOperadoras() {
        this.resultados = [];
        this.erro = "";
        
        if (!this.query.trim()) {
          this.erro = "O campo de busca não pode estar vazio.";
          return;
        }
  
        this.carregando = true;
        
        try {
          const response = await axios.get(
            "http://localhost:8000/buscar-operadoras/", {
              params: { query: this.query },
            }
          );
          this.resultados = response.data;
        } catch (error) {
          console.error("Erro ao buscar operadoras:", error);
          if (error.response && error.response.data) {
            this.erro = error.response.data.detail || "Erro ao buscar operadoras.";
          } else {
            this.erro = "Erro ao conectar com o servidor.";
          }
        } finally {
          this.carregando = false;
        }
      },
    },
  };
  </script>
