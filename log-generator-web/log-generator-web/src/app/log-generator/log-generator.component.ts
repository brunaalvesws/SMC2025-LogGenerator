import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormsModule, NgModel } from '@angular/forms';

interface Activity {
  name: string
  min_duration: number
  max_duration: number
}

@Component({
  selector: 'app-log-generator',
  standalone: true,
  imports: [FormsModule, CommonModule, HttpClientModule],
  templateUrl: './log-generator.component.html',
  styleUrl: './log-generator.component.css'
})
export class LogGeneratorComponent implements OnInit{
  traces = 100
  minEvents = 500
  maxEvents = 1000
  showActivities = false
  declareModel = ''
  arquivoDeclare = ''
  arquivoAcesso = ''
  arquivoOrganizacional = ''

  activities: Activity[] = []

  constructor(private http: HttpClient) {}

  ngOnInit(): void {}

  toggleActivities(): void {
    this.showActivities = !this.showActivities
  }

  handleFileChange(event: any, fileType: string): void {
    console.log(fileType, event.target.files)
  }

  parseActivities(text: string): Activity[] {
    const lines = text.split(/\r?\n/);
    const activities: Activity[] = [];

    for (const line of lines) {
      if (line.startsWith('activity ')) {
        const name = line.slice('activity '.length).trim(); 
        activities.push({
          name,
          min_duration: 1,
          max_duration: 1
        });
      }
    }
    return activities;
  }

  onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0];
    if (file) {
      const reader = new FileReader();
      this.arquivoDeclare = file.name;
      reader.onload = () => {
        this.declareModel = reader.result as string;
        this.activities = this.parseActivities(this.declareModel);
      };
      reader.readAsText(file);
    }
  }

  onFileInputClick(inputId: string): void {
    document.getElementById(inputId)?.click()
  }

  handleMinDurationChange(index: number, event: any): void {
    const newDuration = Number.parseFloat(event.target.value)
    this.activities[index].min_duration = newDuration

    if (this.activities[index].min_duration > this.activities[index].max_duration) {
      this.activities[index].max_duration = this.activities[index].min_duration
    }
  }

  handleMaxDurationChange(index: number, event: any): void {
    const newDuration = Number.parseFloat(event.target.value)
    this.activities[index].max_duration = newDuration
  }

  // Ensure min doesn't exceed max
  onMinEventsChange(event: any): void {
    const value = Number.parseInt(event.target.value)
    this.minEvents = value

    if (this.minEvents > this.maxEvents) {
      this.maxEvents = this.minEvents
    }
  }

  downloadCSV() {
    const formData = new FormData();
    formData.append('files', 'arquivos'); 
    this.http.post('http://localhost:5000/generate-csv', formData, { //colocar isso aqui depois que apertar o botão
      responseType: 'blob'  
    }).subscribe(blob => {
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'resultado.csv';
      a.click();
      window.URL.revokeObjectURL(url);
    });
  }

}


