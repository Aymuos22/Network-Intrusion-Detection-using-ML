import pickle
from pgmpy.inference import VariableElimination
from scapy.all import sniff, conf, get_if_list

# Load the Bayesian Network model
def load_bayesian_model():
    try:
        with open('bayesian_model.pkl', 'rb') as f:
            model = pickle.load(f)
        print("Bayesian model loaded successfully.")
        return model
    except FileNotFoundError:
        print("Error: 'bayesian_model.pkl' not found. Ensure the model file is in the correct location.")
        return None

# Initialize Bayesian model and inference object
bayesian_model = load_bayesian_model()
if bayesian_model:
    inference = VariableElimination(bayesian_model)

# Preprocess the packet to extract relevant features
def preprocess_packet(packet):
    try:
        packet_data = {
            'Protocol': packet.proto if hasattr(packet, 'proto') else 0,
            'TTL': packet.ttl if hasattr(packet, 'ttl') else 64,  # Default TTL
            'Packet Length': len(packet)
        }
        return packet_data
    except Exception as e:
        print(f"Error processing packet: {e}")
        return None

# Function to detect intrusion using Bayesian inference
def detect_intrusion(packet_data):
    try:
        evidence = {
            'Protocol': packet_data['Protocol'],
            'TTL': packet_data['TTL']
        }
        print(f"Performing inference with evidence: {evidence}")
        result = inference.query(variables=['Intrusion'], evidence=evidence)
        
        # Extract probability of intrusion
        intrusion_prob = result.values[1]  # Probability of intrusion = 1
        if intrusion_prob > 0.5:  # Threshold for detection
            print(f"Intrusion Detected with probability {intrusion_prob}")
        else:
            print("No Intrusion Detected")
    except Exception as e:
        print(f"Error during inference: {e} with evidence {evidence}")

# Real-time packet processing function
def process_packet(packet):
    packet_data = preprocess_packet(packet)
    if packet_data:
        detect_intrusion(packet_data)

# Configure Scapy to use Layer 3 socket to avoid Layer 2 compatibility issues
conf.L3socket = conf.L3socket

# List available interfaces and set the chosen interface
available_interfaces = get_if_list()
print("Available interfaces:", available_interfaces)

# Optionally select an interface or use the first available one as a fallback
interface_name = '\\Device\\NPF_{EE991A29-203B-4ABB-8F47-B808BE516FC7}'
if interface_name not in available_interfaces:
    print(f"Specified interface '{interface_name}' not found. Defaulting to first available interface.")
    interface_name = available_interfaces[0]  # Use the first interface as a fallback

print(f"Starting real-time packet capture on {interface_name}... Press Ctrl+C to stop.")

# Start packet capture with error handling
try:
    sniff(iface=interface_name, prn=process_packet, store=0)
except Exception as e:
    print(f"Error during packet capture: {e}")
