import { Routes } from '@angular/router';
import { LogGeneratorComponent } from './log-generator/log-generator.component';

export const routes: Routes = [
    {
        path: 'generate',
        component: LogGeneratorComponent,
        title: 'Log Generator',
    },
];
