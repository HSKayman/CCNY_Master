import torch
import torchvision
from torchvision import datasets, transforms
from torch import nn, optim
import torch.nn.functional as F
from PIL import Image
import torchvision.transforms.functional as TF

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(28 * 28, 512)
        self.fc2 = nn.Linear(512, 256)
        self.fc3 = nn.Linear(256, 10)  

    def forward(self, x):
        x = x.view(-1, 28 * 28)  
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return F.log_softmax(x, dim=1)

transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])

trainset = datasets.MNIST('', download=True, train=True, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=64, shuffle=True)

model = Net()
optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.9)

criterion = nn.NLLLoss()

epochs = 5
for e in range(epochs):
    running_loss = 0
    for images, labels in trainloader:
        optimizer.zero_grad()
        
        output = model(images)
        loss = criterion(output, labels)
        
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
    else:
        print(f"Training loss: {running_loss/len(trainloader)}")

def predict_image(image_path, model):
    transform = transforms.Compose([
        transforms.Grayscale(),  
        transforms.Resize((28, 28)),  
        transforms.ToTensor(),  
        transforms.Normalize((0.5,), (0.5,))  
    ])
    
    image = Image.open(image_path)
    image = transform(image).float()
    image = image.unsqueeze(0)  
    
    with torch.no_grad():
        logps = model(image)
    
    ps = torch.exp(logps)
    
    probab, predicted_class = torch.max(ps, 1)
    
    return probab, predicted_class.item()

image_path = ''  # Update this path to your image
predicted_value = predict_image(image_path, model)
print(f"{predicted_value}")