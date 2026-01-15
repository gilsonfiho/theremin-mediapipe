use_osc "127.0.0.1", 4560

live_loop :theremin_control do
  use_real_time
  
  # 1. Sincronização (Igual ao seu original)
  pitch_rx, volume_rx = sync "/osc*/play_note"
  
  # 2. Tratamento de volume
  audible_volume = [[volume_rx, 0.0].max, 1.0].min
  
  # 3. Efeitos PSICODÉLICOS (Colocados dentro para processar cada nota)
  # O 'distortion' dá o som de guitarra, o 'echo' dá a viagem.
  with_fx :distortion, distort: 0.5 do
    with_fx :echo, phase: 0.25, decay: 2, mix: 0.4 do
      
      # Usando o :prophet que tem um timbre de "guitarra synth" bem psicodélico
      use_synth :prophet
      
      play pitch_rx,
        amp: audible_volume,
        attack: 0.1,    # Ataque rápido para sentir a nota
        sustain: 0.1,
        release: 0.4,   # Um pouco mais de cauda para o eco pegar
        cutoff: 110,    # Abre o som para ficar mais brilhante
        res: 0.7        # Ressonância para dar caráter
      
    end
  end
  
  # Logs para você ver no console se os dados estão chegando
  puts "!!!! Guitarra Ativada - Pitch: #{pitch_rx} !!!!"
end