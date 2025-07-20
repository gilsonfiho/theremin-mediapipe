use_osc "127.0.0.1", 4560

live_loop :theremin_control do
  use_real_time
  
  puts "--> [Sonic Pi] Aguardando mensagem OSC em /osc*/play_note..."
  
  pitch_rx, volume_rx = sync "/osc*/play_note"
  
  puts "!!!! [Sonic Pi] MENSAGEM OSC RECEBIDA E PROCESSADA !!!!"
  puts "!!!! [Sonic Pi] Dados recebidos: Pitch=#{pitch_rx}, Volume=#{volume_rx}"
  
  
  audible_volume = [volume_rx, 0.0].max
  audible_volume = [audible_volume, 1.0].min
  
  
  use_synth :tb303
  play pitch_rx,
    amp: audible_volume,
    attack: 0.5,
    sustain: 0.05,
    release: 0.05,
    vibrato_rate: 12,
    vibrato_depth: 0.5,
    portamento: 0.02
  
  sleep 0.2 # Pequeno delay
end