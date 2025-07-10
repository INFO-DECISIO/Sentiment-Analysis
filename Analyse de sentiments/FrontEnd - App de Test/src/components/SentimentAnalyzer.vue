<template>
  <div class="sentiment-analyzer-container">
    <div class="analyzer-card" :class="{ 'analyzer-card-expanded': message.length > 0 }">
      
      <!-- Header avec titre et sous-titre -->
      <div class="analyzer-header">
        <h1>Analyseur de Sentiment IA</h1>
        <p>Découvrez l'émotion contenue dans votre texte en temps réel</p>
      </div>
      
      <!-- Zone de saisie avec effets -->
      <div class="input-container">
        <textarea 
          v-model="message" 
          @input="onInput" 
          placeholder="Écrivez quelque chose ici..." 
          class="text-input"
          :class="{ 'text-input-active': message.length > 0 }"
        ></textarea>
        
        <!-- Indicateur de caractères restants -->
        <div class="character-counter" :class="{ 
          'warning': message.length > 300 && message.length <= 400,
          'danger': message.length > 400
        }">
          {{ message.length }} / 500
        </div>
      </div>
      
      <!-- Conteneur principal pour l'émoji et les résultats -->
      <transition name="fade-scale">
        <div v-if="isAnalyzing" class="analyzing-container">
          <div class="pulse-rings">
            <div class="ring"></div>
            <div class="ring"></div>
            <div class="ring"></div>
          </div>
          <p>Analyse en cours...</p>
        </div>
        
        <div v-else-if="sentiment && message.length > 0" class="result-container">
          <!-- Émoji grand format avec animation -->
          <transition name="emoji-bounce">
            <div class="emoji-container" :class="`emoji-${sentiment.label}`">
              <span class="emoji" v-html="getEmojiForSentiment"></span>
              
              <!-- Onde d'émotion animée -->
              <div class="emotion-wave" :class="`wave-${sentiment.label}`"></div>
            </div>
          </transition>
          
          <!-- Texte du sentiment -->
          <div class="sentiment-text" :class="`text-${sentiment.label}`">
            {{ getSentimentText }}
          </div>
          
          <!-- Graphique de confiance -->
          <div class="confidence-container">
            <div class="confidence-bar-container">
              <div class="confidence-label">Niveau de confiance</div>
              <div class="confidence-bar">
                <div 
                  class="confidence-fill" 
                  :class="`fill-${sentiment.label}`"
                  :style="{ width: `${confidence}%` }"
                >
                  <div class="confidence-glow" :class="`glow-${sentiment.label}`"></div>
                </div>
              </div>
              <div class="confidence-value">{{ confidence }}%</div>
            </div>
            
            <!-- Graphique de distribution des probabilités -->
            <div v-if="allProbabilities" class="distribution-container">
              <h3>Distribution des probabilités</h3>
              <div class="distribution-chart">
                <DoughnutChart :chartData="chartData" :options="chartOptions" />
              </div>
            </div>
          </div>
        </div>
        
        <div v-else-if="message.length === 0" class="waiting-container">
          <div class="waiting-emoji">🤔</div>
          <p>En attente de votre texte...</p>
        </div>
      </transition>
      
      <!-- Actions et boutons -->
      <div class="action-buttons" v-if="message.length > 0">
        <button class="clear-button" @click="clearText">
          <span class="icon">×</span> Effacer
        </button>
        <button class="analyze-button" @click="forceAnalyze" :disabled="isAnalyzing">
          <span class="icon">↻</span> Ré-analyser
        </button>
      </div>
      
      <!-- Footer avec crédits -->
      <div class="analyzer-footer">
        <p>Projet d'Informatique Décisionnelle - IA d'analyse de sentiment</p>
        <div class="ai-badge">
          <span class="badge-icon">🧠</span> Modèle ML avancé
        </div>
      </div>
      
    </div>
  </div>
</template>

<script>
import { gsap } from 'gsap';
import axios from 'axios';
import debounce from 'lodash.debounce';
import { DoughnutChart } from 'vue-chart-3';
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);

export default {
  name: 'SentimentAnalyzer',
  components: {
    DoughnutChart
  },
  data() {
    return {
      message: '',
      sentiment: null,
      confidence: 0,
      allProbabilities: null,
      isAnalyzing: false,
      apiBaseUrl: 'http://127.0.0.1:5000', // Modifie selon ton API
      chartData: {
        labels: ['Neutre', 'Positif', 'Négatif'],
        datasets: [{
          data: [0, 0, 0],
          backgroundColor: ['#64748b', '#22c55e', '#ef4444']
        }]
      },
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '70%',
        plugins: {
          legend: {
            display: true,
            position: 'bottom'
          }
        }
      }
    };
  },
  computed: {
    getEmojiForSentiment() {
      if (!this.sentiment) return '😶';
      
      switch (this.sentiment.label) {
        case 'positive':
          return this.confidence > 85 ? '😍' : '😊';
        case 'negative':
          return this.confidence > 85 ? '😡' : '😔';
        case 'neutral':
          return '😐';
        case 'undetermined':
          return '🤔';
        default:
          return '😶';
      }
    },
    getSentimentText() {
      if (!this.sentiment) return '';
      
      const intensityPrefix = this.confidence >= 85 ? 'très ' : 
                             this.confidence >= 70 ? 'plutôt ' : '';
      
      switch (this.sentiment.label) {
        case 'positive':
          return `Votre message est ${intensityPrefix}positif`;
        case 'negative':
          return `Votre message est ${intensityPrefix}négatif`;
        case 'neutral':
          return 'Votre message est neutre';
        case 'undetermined':
          return 'Le sentiment est indéterminé';
        default:
          return 'Analyse non concluante';
      }
    }
  },
  created() {
    // Crée une version debounce de la fonction d'analyse
    this.debouncedAnalyze = debounce(this.analyzeSentiment, 600);
  },
  methods: {
    onInput() {
      if (this.message.trim() === '') {
        this.sentiment = null;
        this.confidence = 0;
        this.allProbabilities = null;
        return;
      }
      
      this.isAnalyzing = true;
      this.debouncedAnalyze();
    },
    
    forceAnalyze() {
      if (this.message.trim() === '') return;
      
      this.isAnalyzing = true;
      // Annule le debounce et lance immédiatement l'analyse
      this.debouncedAnalyze.cancel();
      this.analyzeSentiment();
    },
    
    async analyzeSentiment() {
      try {
        // Appel à ton API Flask
        const response = await axios.post(`${this.apiBaseUrl}/test-predict`, {
          text: this.message
        });
        
        if (response.data.success) {
          // Animation des résultats
          this.animateResults(response.data);
        } else {
          console.error('Erreur API:', response.data.error);
          this.sentiment = { label: 'undetermined', value: null };
          this.confidence = 0;
        }
      } catch (error) {
        console.error('Erreur lors de la requête API:', error);
        this.sentiment = { label: 'undetermined', value: null };
        this.confidence = 0;
      } finally {
        this.isAnalyzing = false;
      }
    },
    
    animateResults(data) {
      // Récupère les données de l'API
      const newSentiment = data.result;
      const newConfidence = Math.round(data.probability * 100);
      const probabilities = data.all_probabilities;
      
      // Met à jour le graphique si des probabilités sont disponibles
      if (probabilities && probabilities.length === 3) {
        // Transforme les probabilités en pourcentages
        const percentages = probabilities.map(p => Math.round(p * 100));
        
        // Animation du graphique
        this.chartData = {
          ...this.chartData,
          datasets: [{
            data: percentages,
            backgroundColor: ['#64748b', '#22c55e', '#ef4444']
          }]
        };
        this.allProbabilities = percentages;
      }
      
      // Animation du niveau de confiance avec GSAP
      gsap.to(this, {
        confidence: newConfidence,
        duration: 1,
        ease: 'power2.out'
      });
      
      // Met à jour le sentiment
      this.sentiment = newSentiment;
    },
    
    clearText() {
      // Animation pour effacer le texte
      gsap.to(this, {
        duration: 0.3,
        onComplete: () => {
          this.message = '';
          this.sentiment = null;
          this.confidence = 0;
          this.allProbabilities = null;
        }
      });
    }
  }
};
</script>

<style scoped>
/* === CONTAINER PRINCIPAL === */
.sentiment-analyzer-container {
  width: 100%;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #1e293b, #0f172a);
  padding: 2rem;
  font-family: 'Inter', 'Segoe UI', sans-serif;
}

.analyzer-card {
  width: 100%;
  max-width: 800px;
  min-height: 600px;
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(10px);
  border-radius: 24px;
  box-shadow: 
    0 20px 60px rgba(0, 0, 0, 0.3),
    0 5px 15px rgba(0, 0, 0, 0.2),
    inset 0 1px 2px rgba(255, 255, 255, 0.1);
  padding: 2.5rem;
  color: #f8fafc;
  transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  display: flex;
  flex-direction: column;
  gap: 2rem;
  position: relative;
  overflow: hidden;
}

.analyzer-card::before {
  content: '';
  position: absolute;
  top: -30%;
  left: -30%;
  width: 160%;
  height: 160%;
  background: radial-gradient(
    circle at 50% 0%,
    rgba(56, 189, 248, 0.1) 0%,
    rgba(0, 0, 0, 0) 70%
  );
  z-index: -1;
}

.analyzer-card-expanded {
  transform: scale(1.02);
}

/* === HEADER === */
.analyzer-header {
  text-align: center;
  margin-bottom: 1rem;
}

.analyzer-header h1 {
  font-size: 2.5rem;
  font-weight: 700;
  background: linear-gradient(45deg, #38bdf8, #818cf8);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  margin-bottom: 0.5rem;
  letter-spacing: -0.02em;
}

.analyzer-header p {
  color: #cbd5e1;
  font-size: 1.1rem;
  max-width: 500px;
  margin: 0 auto;
}

/* === ZONE DE SAISIE === */
.input-container {
  position: relative;
  width: 100%;
  margin-bottom: 1rem;
}

.text-input {
  width: 100%;
  min-height: 120px;
  padding: 1.25rem;
  border-radius: 16px;
  background: rgba(30, 41, 59, 0.7);
  color: #f1f5f9;
  font-size: 1.1rem;
  line-height: 1.6;
  border: 1px solid rgba(148, 163, 184, 0.2);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  resize: vertical;
}

.text-input:focus {
  outline: none;
  border-color: #38bdf8;
  box-shadow: 
    0 0 0 3px rgba(56, 189, 248, 0.3),
    0 4px 12px rgba(0, 0, 0, 0.1);
}

.text-input-active {
  border-color: #38bdf8;
}

.character-counter {
  position: absolute;
  right: 15px;
  bottom: 15px;
  font-size: 0.9rem;
  color: #94a3b8;
  background-color: rgba(15, 23, 42, 0.7);
  padding: 4px 10px;
  border-radius: 20px;
  transition: all 0.3s ease;
}

.character-counter.warning {
  color: #fbbf24;
}

.character-counter.danger {
  color: #ef4444;
}

/* === RÉSULTATS === */
.result-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
  padding: 1rem 0;
}

.emoji-container {
  position: relative;
  width: 150px;
  height: 150px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 1rem;
}

.emoji {
  font-size: 6rem;
  filter: drop-shadow(0 10px 15px rgba(0, 0, 0, 0.2));
  z-index: 1;
}

.emotion-wave {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  opacity: 0.3;
  z-index: 0;
  animation: pulse 3s infinite ease-in-out;
}

@keyframes pulse {
  0% {
    transform: scale(0.95);
    opacity: 0.7;
  }
  50% {
    transform: scale(1.05);
    opacity: 0.4;
  }
  100% {
    transform: scale(0.95);
    opacity: 0.7;
  }
}

.wave-positive {
  background: radial-gradient(circle, rgba(34, 197, 94, 0.7) 0%, rgba(34, 197, 94, 0) 70%);
  box-shadow: 0 0 30px rgba(34, 197, 94, 0.5);
}

.wave-negative {
  background: radial-gradient(circle, rgba(239, 68, 68, 0.7) 0%, rgba(239, 68, 68, 0) 70%);
  box-shadow: 0 0 30px rgba(239, 68, 68, 0.5);
}

.wave-neutral {
  background: radial-gradient(circle, rgba(148, 163, 184, 0.7) 0%, rgba(148, 163, 184, 0) 70%);
  box-shadow: 0 0 30px rgba(148, 163, 184, 0.5);
}

.wave-undetermined {
  background: radial-gradient(circle, rgba(234, 179, 8, 0.7) 0%, rgba(234, 179, 8, 0) 70%);
  box-shadow: 0 0 30px rgba(234, 179, 8, 0.5);
}

.sentiment-text {
  font-size: 1.5rem;
  font-weight: 600;
  text-align: center;
  margin-bottom: 1rem;
}

.text-positive {
  color: #22c55e;
}

.text-negative {
  color: #ef4444;
}

.text-neutral {
  color: #94a3b8;
}

.text-undetermined {
  color: #eab308;
}

/* === CONFIDENCE BAR === */
.confidence-container {
  width: 100%;
  max-width: 500px;
}

.confidence-bar-container {
  margin-bottom: 2rem;
}

.confidence-label {
  font-size: 0.9rem;
  color: #94a3b8;
  margin-bottom: 0.5rem;
}

.confidence-bar {
  height: 12px;
  background: rgba(30, 41, 59, 0.7);
  border-radius: 20px;
  overflow: hidden;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.3);
}

.confidence-fill {
  height: 100%;
  border-radius: 20px;
  position: relative;
  transition: width 1s cubic-bezier(0.19, 1, 0.22, 1);
}

.fill-positive {
  background: linear-gradient(90deg, #15803d, #22c55e);
}

.fill-negative {
  background: linear-gradient(90deg, #b91c1c, #ef4444);
}

.fill-neutral {
  background: linear-gradient(90deg, #475569, #64748b);
}

.fill-undetermined {
  background: linear-gradient(90deg, #ca8a04, #eab308);
}

.confidence-glow {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-size: 200% 100%;
  background-position: right;
  animation: shimmer 2s infinite;
  opacity: 0.5;
}

@keyframes shimmer {
  0% {
    background-position: -100% 0;
  }
  100% {
    background-position: 100% 0;
  }
}

.glow-positive {
  background-image: linear-gradient(90deg, transparent, rgba(34, 197, 94, 0.6), transparent);
}

.glow-negative {
  background-image: linear-gradient(90deg, transparent, rgba(239, 68, 68, 0.6), transparent);
}

.glow-neutral {
  background-image: linear-gradient(90deg, transparent, rgba(148, 163, 184, 0.6), transparent);
}

.glow-undetermined {
  background-image: linear-gradient(90deg, transparent, rgba(234, 179, 8, 0.6), transparent);
}

.confidence-value {
  text-align: right;
  font-size: 1rem;
  font-weight: 600;
  margin-top: 0.5rem;
  color: #e2e8f0;
}

/* === DISTRIBUTION CHART === */
.distribution-container {
  width: 100%;
  margin-top: 1rem;
}

.distribution-container h3 {
  font-size: 1rem;
  color: #94a3b8;
  text-align: center;
  margin-bottom: 1rem;
}

.distribution-chart {
  height: 180px;
  width: 100%;
}

/* === WAITING & ANALYZING === */
.waiting-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 300px;
}

.waiting-emoji {
  font-size: 4rem;
  margin-bottom: 1rem;
  opacity: 0.7;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
  100% {
    transform: translateY(0px);
  }
}

.waiting-container p {
  color: #94a3b8;
}

.analyzing-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 300px;
}

.pulse-rings {
  position: relative;
  width: 80px;
  height: 80px;
  margin-bottom: 1.5rem;
}

.ring {
  position: absolute;
  border-radius: 50%;
  border: 2px solid #38bdf8;
  width: 100%;
  height: 100%;
  opacity: 0;
  animation: pulseRing 2s cubic-bezier(0.455, 0.03, 0.515, 0.955) infinite;
}

.ring:nth-child(2) {
  animation-delay: 0.66s;
}

.ring:nth-child(3) {
  animation-delay: 1.33s;
}

@keyframes pulseRing {
  0% {
    transform: scale(0.5);
    opacity: 0;
  }
  50% {
    opacity: 0.5;
  }
  100% {
    transform: scale(1.5);
    opacity: 0;
  }
}

.analyzing-container p {
  color: #94a3b8;
  font-size: 1.1rem;
}

/* === BUTTONS === */
.action-buttons {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 1rem;
}

.clear-button, .analyze-button {
  padding: 0.75rem 1.5rem;
  border-radius: 12px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  border: none;
}

.clear-button {
  background-color: rgba(239, 68, 68, 0.15);
  color: #ef4444;
}

.clear-button:hover {
  background-color: rgba(239, 68, 68, 0.25);
}

.analyze-button {
  background-color: rgba(56, 189, 248, 0.15);
  color: #38bdf8;
}

.analyze-button:hover {
  background-color: rgba(56, 189, 248, 0.25);
}

.analyze-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.icon {
  font-size: 1.1rem;
}

/* === FOOTER === */
.analyzer-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
  padding-top: 1rem;
  border-top: 1px solid rgba(148, 163, 184, 0.1);
  font-size: 0.85rem;
  color: #64748b;
}

.ai-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: rgba(56, 189, 248, 0.15);
  padding: 0.5rem 0.75rem;
  border-radius: 20px;
  color: #38bdf8;
  font-weight: 600;
  font-size: 0.85rem;
}

.badge-icon {
  font-size: 1rem;
}

/* === ANIMATIONS === */
.fade-scale-enter-active,
.fade-scale-leave-active {
  transition: all 0.4s ease;
}

.fade-scale-enter-from,
.fade-scale-leave-to {
  opacity: 0;
  transform: scale(0.9);
}

.emoji-bounce-enter-active {
  animation: bounce 0.6s;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-30px);
  }
  60% {
    transform: translateY(-15px);
  }
}

/* === RESPONSIVE DESIGN === */
@media (max-width: 768px) {
  .analyzer-card {
    padding: 1.5rem;
    gap: 1.5rem;
  }

  .analyzer-header h1 {
    font-size: 1.8rem;
  }
  
  .emoji {
    font-size: 5rem;
  }
  
  .sentiment-text {
    font-size: 1.2rem;
  }
  
  .emoji-container {
    width: 120px;
    height: 120px;
  }
  
  .distribution-chart {
    height: 150px;
  }
}

@media (max-width: 480px) {
  .sentiment-analyzer-container {
    padding: 1rem;
  }
  
  .analyzer-card {
    padding: 1.25rem;
    gap: 1.25rem;
  }
  
  .analyzer-header h1 {
    font-size: 1.5rem;
  }
  
  .analyzer-header p {
    font-size: 0.95rem;
  }
  
  .text-input {
    min-height: 100px;
    padding: 1rem;
    font-size: 1rem;
  }
  
  .emoji {
    font-size: 4rem;
  }
  
  .action-buttons {
    flex-direction: column;
    width: 100%;
  }
  
  .clear-button, .analyze-button {
    width: 100%;
    justify-content: center;
  }
}
</style>