import argparse

from datasets import load_dataset, Audio
from transformers import (
    WhisperForConditionalGeneration,
    WhisperProcessor,
    TrainingArguments,
    Trainer,
)


def parse_args():
    parser = argparse.ArgumentParser(description="Fine-tune a Whisper ASR model")
    parser.add_argument("--dataset", required=True, help="Path or dataset identifier")
    parser.add_argument("--output", required=True, help="Directory to save the fine-tuned model")
    parser.add_argument(
        "--model-name",
        default="openai/whisper-base",
        help="Model name or path to the base checkpoint",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    ds = load_dataset(args.dataset)
    ds = ds.cast_column("audio", Audio(sampling_rate=16000))

    processor = WhisperProcessor.from_pretrained(args.model_name)
    model = WhisperForConditionalGeneration.from_pretrained(args.model_name)

    def preprocess(batch):
        audio = batch["audio"]
        inputs = processor(
            audio["array"], sampling_rate=audio["sampling_rate"], return_tensors="pt"
        )
        batch["input_features"] = inputs.input_features[0]
        with processor.as_target_processor():
            batch["labels"] = processor(batch["text"]).input_ids
        return batch

    ds = ds.map(preprocess)

    training_args = TrainingArguments(
        output_dir=args.output,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        num_train_epochs=1,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        logging_steps=10,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=ds.get("train"),
        eval_dataset=ds.get("validation"),
    )

    trainer.train()
    trainer.save_model(args.output)
    processor.save_pretrained(args.output)


if __name__ == "__main__":
    main()
