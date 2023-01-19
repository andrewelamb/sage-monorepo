import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UiModule } from '@sagebionetworks/openchallenges/ui';
import { FeaturedChallengeListComponent } from './featured-challenge-list.component';

@NgModule({
  declarations: [FeaturedChallengeListComponent],
  imports: [CommonModule, UiModule],
  exports: [FeaturedChallengeListComponent],
})
export class FeaturedChallengeListModule {}