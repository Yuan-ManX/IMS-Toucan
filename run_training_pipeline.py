import argparse
import sys

import torch

from Pipelines.Pipeline_FastSpeech2_LJSpeech import run as fast_LJSpeech
from Pipelines.Pipeline_FastSpeech2_LibriTTS import run as fast_LibriTTS
from Pipelines.Pipeline_FastSpeech2_Nancy import run as fast_Nancy
from Pipelines.Pipeline_FastSpeech2_Thorsten import run as fast_Thorsten
from Pipelines.Pipeline_IntegrationTest import run as integration_test
from Pipelines.Pipeline_MelGAN_LJSpeech import run as melgan_LJSpeech
from Pipelines.Pipeline_MelGAN_Nancy import run as melgan_Nancy
from Pipelines.Pipeline_MelGAN_Thorsten import run as melgan_Thorsten
from Pipelines.Pipeline_MelGAN_combined import run as melgan_combined
from Pipelines.Pipeline_TransformerTTS_LJSpeech import run as trans_LJSpeech
from Pipelines.Pipeline_TransformerTTS_LibriTTS import run as trans_LibriTTS
from Pipelines.Pipeline_TransformerTTS_Nancy import run as trans_Nancy
from Pipelines.Pipeline_TransformerTTS_Thorsten import run as trans_Thorsten

pipeline_dict = {
    "fast_Thorsten"   : fast_Thorsten,
    "melgan_Thorsten" : melgan_Thorsten,
    "trans_Thorsten"  : trans_Thorsten,

    "fast_LibriTTS"   : fast_LibriTTS,
    "trans_LibriTTS"  : trans_LibriTTS,

    "fast_LJSpeech"   : fast_LJSpeech,
    "melgan_LJSpeech" : melgan_LJSpeech,
    "trans_LJSpeech"  : trans_LJSpeech,

    "fast_Nancy"      : fast_Nancy,
    "melgan_Nancy"    : melgan_Nancy,
    "trans_Nancy"     : trans_Nancy,

    "integration_test": integration_test,
    "melgan_combined" : melgan_combined,
    }

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='IMS Speech Synthesis Toolkit - Call to Train')

    parser.add_argument('pipeline',
                        choices=list(pipeline_dict.keys()),
                        help="Select pipeline to train.")

    parser.add_argument('--gpu_id',
                        type=str,
                        help="Which GPU to run on. If not specified runs on CPU, but other than for integration tests that doesn't make much sense.",
                        default="cpu")

    parser.add_argument('--resume_checkpoint',
                        type=str,
                        help="Path to checkpoint to resume from.",
                        default=None)

    parser.add_argument('--finetune',
                        action="store_true",
                        help="Whether to fine-tune from the specified checkpoint.",
                        default=False)

    parser.add_argument('--model_save_dir',
                        type=str,
                        help="Directory where the checkpoints should be saved to.",
                        default=None)

    args = parser.parse_args()

    if args.finetune and args.resume_checkpoint is None:
        print("Need to provide path to checkpoint to fine-tune from!")
        sys.exit()

    if args.finetune and "melgan" in args.pipeline:
        print("Fine-tuning for MelGAN is not implemented as it didn't seem necessary and the GAN would most likely fail. Just train from scratch.")
        sys.exit()

    if "fast" in args.pipeline:
        torch.multiprocessing.set_start_method('spawn', force=False)

    pipeline_dict[args.pipeline](gpu_id=args.gpu_id, resume_checkpoint=args.resume_checkpoint, finetune=args.finetune, model_dir=args.model_save_dir)
