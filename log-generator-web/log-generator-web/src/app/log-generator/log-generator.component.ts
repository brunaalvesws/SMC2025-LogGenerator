import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormsModule, NgModel } from '@angular/forms';


interface Activity {
  name: string
  duration: number
}

@Component({
  selector: 'app-log-generator',
  standalone: true,
  imports: [FormsModule, CommonModule],
  templateUrl: './log-generator.component.html',
  styleUrl: './log-generator.component.css'
})
export class LogGeneratorComponent implements OnInit{
  traces = 100
  minEvents = 500
  maxEvents = 1000
  showActivities = false

  activities: Activity[] = [
    { name: "Documentação de Requisitos", duration: 4 },
    { name: "Manutenção de Funcionalidade", duration: 6 },
    { name: "Contagem de Ponto de Função", duration: 3 },
    { name: "Executar testes", duration: 5 },
    { name: "Análise de Requisitos", duration: 8 },
  ]

  constructor() {}

  ngOnInit(): void {}

  toggleActivities(): void {
    this.showActivities = !this.showActivities
  }

  handleFileChange(event: any, fileType: string): void {
    console.log(fileType, event.target.files)
  }

  onFileInputClick(inputId: string): void {
    document.getElementById(inputId)?.click()
  }

  handleDurationChange(index: number, event: any): void {
    const newDuration = Number.parseFloat(event.target.value)
    this.activities[index].duration = newDuration
  }

  // Ensure min doesn't exceed max
  onMinEventsChange(event: any): void {
    const value = Number.parseInt(event.target.value)
    this.minEvents = value

    if (this.minEvents > this.maxEvents) {
      this.maxEvents = this.minEvents
    }
  }
}


