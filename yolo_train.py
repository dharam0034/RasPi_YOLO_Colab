from ultralytics import YOLO
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="YOLO trainer")
    parser.add_argument("--config", type=str, default="config.yaml", help="The dataset config file")
    parser.add_argument("--init_model", type=str, default="yolo11n.pt", help="The pre-trained model weights")

    parser.add_argument("--name", type=str, default="yolo", help="Save dir")
    parser.add_argument("--epochs", type=int, default=20, help="Number of training epochs")
    parser.add_argument("--device", type=int, default=0, help="Device training index")

    parser.add_argument("--export_format", type=str, default="onnx", help="format to export the model as, eg onnx, imx")
    parser.add_argument("--export_config", type=str, default=None, help="The dataset config file for export")
    parser.add_argument("--resume_training",  action='store_true', help="Resume training of a model")
    parser.add_argument("--export_only",  action='store_true', help="Just export the weights as onnx")
    parser.add_argument("--int8_weights",  action='store_true', help="Export the weights as int8")
    parser.add_argument("--image_size", type=int, default=640, help="Input image size")
    parser.add_argument("--val_model",  action='store_true', help="Validate the model only")

    return parser.parse_args()


def main():
    args = parse_arguments()

    # Load a YOLOv8n PyTorch model
    model = YOLO(args.init_model)

    if not args.export_only and not args.val_model:
        if args.resume_training:
            project = args.name
        else:
            project = None

        _ = model.train(data=args.config, epochs=args.epochs, imgsz=args.image_size, save=True,
                              device=args.device, name=args.name, batch=0.9, resume=args.resume_training,
                              cache=False, project=project)
    elif  args.val_model:
        _ = model.val(name=args.name, project=args.name)  # no arguments needed, dataset and settings remembered

    # Export the model
    if args.export_format:
        model.export(format=args.export_format, int8=args.int8_weights, imgsz=args.image_size, device=0, batch=16, nms=True,
                     data=args.export_config, opset=11)  # exports with PTQ quantization by default

if __name__ == "__main__":
    main()