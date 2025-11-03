#!/usr/bin/env python3
"""Create a sample PDF for testing."""

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch

# Create PDF
doc = SimpleDocTemplate("examples/sample_paper.pdf", pagesize=letter)
styles = getSampleStyleSheet()
story = []

# Title
title = Paragraph("<b><font size=16>Introduction to Neural Networks</font></b>", styles['Title'])
story.append(title)
story.append(Spacer(1, 0.3*inch))

# Abstract
abstract = Paragraph("<b>Abstract</b>", styles['Heading1'])
story.append(abstract)
content = Paragraph(
    "Neural networks are computational models inspired by biological neural systems. "
    "They consist of interconnected nodes that process information through weighted connections. "
    "This paper provides an overview of fundamental neural network architectures.",
    styles['Normal']
)
story.append(content)
story.append(Spacer(1, 0.2*inch))

# Section 1
section1 = Paragraph("<b>1. Introduction</b>", styles['Heading1'])
story.append(section1)
content1 = Paragraph(
    "Artificial neural networks have revolutionized machine learning by enabling computers "
    "to learn complex patterns from data. The basic building block is the artificial neuron, "
    "which takes multiple inputs and produces a single output.",
    styles['Normal']
)
story.append(content1)
story.append(Spacer(1, 0.2*inch))

# Section 1.1
section11 = Paragraph("<b>1.1 Biological Inspiration</b>", styles['Heading2'])
story.append(section11)
content11 = Paragraph(
    "The architecture of neural networks is inspired by biological neurons in the brain. "
    "Just as biological neurons communicate through synapses, artificial neurons are connected "
    "through weighted links that determine the strength of signal transmission.",
    styles['Normal']
)
story.append(content11)
story.append(Spacer(1, 0.2*inch))

# Section 2
section2 = Paragraph("<b>2. Network Architecture</b>", styles['Heading1'])
story.append(section2)
content2 = Paragraph(
    "Neural networks are organized in layers. The input layer receives data, hidden layers "
    "process information, and the output layer produces predictions. Each layer transforms "
    "the data through mathematical operations.",
    styles['Normal']
)
story.append(content2)
story.append(Spacer(1, 0.2*inch))

# Section 2.1
section21 = Paragraph("<b>2.1 Activation Functions</b>", styles['Heading2'])
story.append(section21)
content21 = Paragraph(
    "Activation functions introduce non-linearity into the network. Common functions include "
    "sigmoid, tanh, and ReLU. The choice of activation function affects the network's ability "
    "to learn complex patterns.",
    styles['Normal']
)
story.append(content21)
story.append(Spacer(1, 0.2*inch))

# Section 2.2
section22 = Paragraph("<b>2.2 Layer Types</b>", styles['Heading2'])
story.append(section22)
content22 = Paragraph(
    "Different layer types serve different purposes. Dense layers connect all neurons, "
    "convolutional layers process spatial data, and recurrent layers handle sequential data. "
    "The architecture choice depends on the problem domain.",
    styles['Normal']
)
story.append(content22)
story.append(Spacer(1, 0.2*inch))

# Section 3
section3 = Paragraph("<b>3. Training Process</b>", styles['Heading1'])
story.append(section3)
content3 = Paragraph(
    "Training adjusts network weights to minimize prediction errors. This involves forward "
    "propagation to compute outputs, loss calculation to measure errors, and backpropagation "
    "to update weights using gradient descent optimization.",
    styles['Normal']
)
story.append(content3)
story.append(Spacer(1, 0.2*inch))

# Section 4
section4 = Paragraph("<b>4. Applications</b>", styles['Heading1'])
story.append(section4)
content4 = Paragraph(
    "Neural networks power many modern AI applications including image recognition, "
    "natural language processing, speech synthesis, and game playing. Their versatility "
    "makes them suitable for a wide range of problems.",
    styles['Normal']
)
story.append(content4)
story.append(Spacer(1, 0.2*inch))

# Conclusion
conclusion = Paragraph("<b>5. Conclusion</b>", styles['Heading1'])
story.append(conclusion)
content5 = Paragraph(
    "Neural networks represent a powerful approach to machine learning. Understanding their "
    "architecture, training process, and applications is essential for modern AI development. "
    "Continued research continues to expand their capabilities and applications.",
    styles['Normal']
)
story.append(content5)

# Build PDF
doc.build(story)
print("Sample PDF created: examples/sample_paper.pdf")
