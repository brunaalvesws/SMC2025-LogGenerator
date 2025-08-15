import { Routes } from '@angular/router';
import { LogGeneratorComponent } from './log-generator/log-generator.component';

export const routes: Routes = [
     {
        path: '',
        redirectTo: 'generate',
        pathMatch: 'full', 
    },
    {
        path: 'generate',
        component: LogGeneratorComponent,
        title: 'Log Generator',
    },
];
