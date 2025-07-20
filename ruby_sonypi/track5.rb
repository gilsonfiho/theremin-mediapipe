use_osc "127.0.0.1", 4560

live_loop :theremin_control do
  use_real_time
  
  
  pitch_rx, volume_rx = sync "/osc*/play_note"
  
  puts "!!!! [Sonic Pi] MENSAGEM OSC RECEBIDA E PROCESSADA !!!!"
  puts "!!!! [Sonic Pi] Dados recebidos: Pitch=#{pitch_rx}, Volume=#{volume_rx}]"
  
  audible_volume = [volume_rx, 0.0].max
  audible_volume = [audible_volume, 1.0].min
  
  with_fx :reverb, room: 0.7, mix: 0.6 do
    use_synth :fm
    play pitch_rx,
      amp: audible_volume,
      attack: 0.01,
      sustain: 0.1,
      release: 0.3,
      
    mod_rate: 0.7,         
      mod_range: 2,           
      
    vibrato_rate: 2,        
      vibrato_depth: 0.08,    
      
    portamento: 0.05,      
      
    cutoff: 100,           
      res: 0 
      
  end 
  
  sleep 0.1 
 
end