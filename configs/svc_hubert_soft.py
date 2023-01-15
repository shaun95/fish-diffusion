from fish_diffusion.utils.pitch import pitch_to_coarse

_base_ = [
    "./_base_/trainers/base.py",
    "./_base_/datasets/audio_folder.py",
]

sampling_rate = 44100
mel_channels = 128
hidden_size = 256

model = dict(
    diffusion=dict(
        type="GaussianDiffusion",
        mel_channels=mel_channels,
        keep_bins=128,
        noise_schedule="linear",
        timesteps=1000,
        max_beta=0.01,
        s=0.008,
        noise_loss="smoothed-l1",
        denoiser=dict(
            type="WaveNetDenoiser",
            mel_channels=mel_channels,
            d_encoder=hidden_size,
            residual_channels=512,
            residual_layers=20,
            dropout=0.2,
        ),
        spec_stats_path="dataset/stats.json",
        sampler_speed_up=10,
    ),
    text_encoder=dict(
        type="NaiveProjectionEncoder",
        input_size=256,
        output_size=256,
    ),
    speaker_encoder=dict(
        type="NaiveProjectionEncoder",
        input_size=10,
        output_size=hidden_size,
        use_embedding=True,
    ),
    pitch_encoder=dict(
        type="NaiveProjectionEncoder",
        input_size=256,
        output_size=hidden_size,
        use_embedding=True,
        preprocessing=pitch_to_coarse,
    ),
    vocoder=dict(
        type="NsfHifiGAN",
        checkpoint_path="checkpoints/nsf_hifigan/model",
        sampling_rate=sampling_rate,
        mel_channels=mel_channels,
    ),
)

preprocessing = dict(
    text_features_extractor=dict(
        type="HubertSoft",
    ),
    pitch_extractor="crepe",
)
